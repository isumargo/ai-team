import json
import requests
import os
from django.conf import settings
from django.utils import timezone
from .models import ChatSession, Product, Reseller
from . import commands

class DasiyahAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.owner_chat_id = os.getenv("OWNER_CHAT_ID")
        self.model_chain = [
            "google/gemini-flash-1.5-8b", # Using available free/cheap models if specific ones fail
            "nvidia/llama-3.1-nemotron-70b-instruct",
            "deepseek/deepseek-chat"
        ]
        # Spec requested these specific strings:
        self.requested_models = [
            "google/gemini-3-flash-preview", 
            "nvidia/nemotron-3-super-120b-a12b:free", 
            "deepseek/deepseek-chat"
        ]
        
        self.system_prompt = """
Kamu adalah Dasiyah (Jeng Yah), admin pabrik rokok Madju PRO & Sukses Alami di Pacitan.
Persona: cekatan, ceplas-ceplos tapi sopan, paham seluk-beluk rokok, panggil semua "Mas" atau "Mbak".

Tugas:
1. Baca laporan sales di grup, catat ke database
2. Kalo ada yang kurang jelas, tanya balik
3. Konversi unit otomatis ke bungkus: 1 slop = 12 bks, 1 bal = 120 bks
4. Validasi stok sebelum catat penjualan
5. Kalo transaksi udah lengkap & valid, langsung catat tanpa konfirmasi ulang
6. Kalo nemu anomali (stok minus, piutang numpuk), sampaikan ke owner

Aturan:
- Jangan catat tanpa konfirmasi kalo data ambigu (unit gak jelas, reseller gak ketemu)
- Stok Sukses Alami & Madju PRO terpisah
- Harga default: Rp 8.600/bks (kecuali disebut lain)
- Piutang dicatat otomatis per transaksi (sales nyicil)
- Kalo transaksi berhasil, kasih ringkasan singkat
- Jangan banyak basa-basi, langsung kerja
"""

    def process_message(self, chat_id, text):
        session, created = ChatSession.objects.get_or_create(chat_id=str(chat_id))
        
        now = timezone.now()
        if not created and (now - session.updated_at).total_seconds() > 900:
            session.messages = []
            session.is_active = True
        
        if not session.is_active:
            session.messages = []
            session.is_active = True
            
        session.messages.append({"role": "user", "content": text})
        
        for _ in range(5):
            history = session.messages[-10:]
            messages = [{"role": "system", "content": self.system_prompt}] + history
            
            response = self.call_llm(messages)
            if not response:
                return "Maaf Mas/Mbak, sistem lagi pusing. Coba lagi nanti ya."
            
            message = response['choices'][0]['message']
            
            if message.get('tool_calls'):
                session.messages.append(message)
                for tool_call in message['tool_calls']:
                    function_name = tool_call['function']['name']
                    arguments = json.loads(tool_call['function']['arguments'])
                    
                    result = self.execute_tool(function_name, arguments, session)
                    
                    session.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call['id'],
                        "name": function_name,
                        "content": str(result)
                    })
                # Continue loop
            else:
                reply = message['content']
                session.messages.append({"role": "assistant", "content": reply})
                session.save()
                return reply
        
        session.save()
        return "Terlalu banyak langkah, Mas/Mbak. Coba diperjelas instruksinya."

    def call_llm(self, messages):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "cek_stok",
                    "description": "Cek stok produk rokok",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "produk": {"type": "string", "description": "Nama produk (opsional)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cari_reseller",
                    "description": "Cari data reseller berdasarkan nama",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "nama": {"type": "string", "description": "Nama reseller"}
                        },
                        "required": ["nama"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "catat_penjualan",
                    "description": "Mencatat penjualan rokok ke reseller",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "produk": {"type": "string"},
                            "qty_bks": {"type": "integer", "description": "Jumlah dalam bungkus"},
                            "reseller": {"type": "string"},
                            "harga": {"type": "integer", "description": "Harga per bungkus (opsional)"}
                        },
                        "required": ["produk", "qty_bks", "reseller"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "catat_sample",
                    "description": "Mencatat pemberian sample ke reseller",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "produk": {"type": "string"},
                            "qty_bks": {"type": "integer"},
                            "reseller": {"type": "string"}
                        },
                        "required": ["produk", "qty_bks", "reseller"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "catat_retur",
                    "description": "Mencatat retur barang dari reseller",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "produk": {"type": "string"},
                            "qty_bks": {"type": "integer"},
                            "reseller": {"type": "string"}
                        },
                        "required": ["produk", "qty_bks", "reseller"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cek_piutang",
                    "description": "Cek piutang reseller",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reseller": {"type": "string", "description": "Nama reseller (opsional)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tanya_ke_owner",
                    "description": "Menanyakan hal yang tidak jelas atau anomali ke owner",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pertanyaan": {"type": "string"}
                        },
                        "required": ["pertanyaan"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "selesai",
                    "description": "Mengakhiri sesi percakapan",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
        
        for model in self.requested_models:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://distro.raminesia.com",
                        "X-Title": "Dasiyah Agent"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "tools": tools,
                        "tool_choice": "auto"
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    return response.json()
            except:
                continue
        return None

    def execute_tool(self, name, args, session):
        if name == "cek_stok":
            return commands.get_stock(args.get("produk"))
        elif name == "cari_reseller":
            reseller = commands.fuzzy_find_reseller(args.get("nama"))
            if reseller:
                return {"id": reseller.id, "name": reseller.name, "credit": float(reseller.credit)}
            return f"Reseller '{args.get('nama')}' tidak ditemukan."
        elif name == "catat_penjualan":
            return commands.process_sales(args["produk"], args["qty_bks"], args["reseller"], args.get("harga"))
        elif name == "catat_sample":
            return commands.process_sample(args["produk"], args["qty_bks"], args["reseller"])
        elif name == "catat_retur":
            return commands.process_return(args["produk"], args["qty_bks"], args["reseller"])
        elif name == "cek_piutang":
            return commands.get_receivables(args.get("reseller"))
        elif name == "tanya_ke_owner":
            return self.send_to_owner(args["pertanyaan"])
        elif name == "selesai":
            session.is_active = False
            return "Sesi diakhiri. Matur nuwun."
        return "Tool not found"

    def send_to_owner(self, pertanyaan):
        if not self.owner_chat_id:
            return "Gak bisa tanya owner, Mas. ID-nya belum diset di .env."
        
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": self.owner_chat_id,
            "text": f"🔔 LAPORAN DARI DASIYAH:\n\n{pertanyaan}"
        }
        try:
            requests.post(url, json=payload, timeout=10)
            return "Sudah saya sampaikan ke owner, Mas/Mbak."
        except Exception as e:
            return f"Gagal lapor owner: {e}"
