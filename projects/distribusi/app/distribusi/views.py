import requests
import json
from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Reseller, Transaction, StockMovement
from .parser import parse_message
from . import commands

def dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=7)

    total_stock = Product.objects.aggregate(s=Sum("stock"))["s"] or 0
    total_resellers = Reseller.objects.filter(active=True).count()
    total_credit = Reseller.objects.aggregate(c=Sum("credit"))["c"] or 0

    revenue_today = Transaction.objects.filter(
        created_at__date=today, payment_status="paid"
    ).aggregate(r=Sum("total"))["r"] or 0

    revenue_week = Transaction.objects.filter(
        created_at__date__gte=week_ago, payment_status="paid"
    ).aggregate(r=Sum("total"))["r"] or 0

    pending_payments = Transaction.objects.filter(
        payment_status="unpaid"
    ).aggregate(p=Sum("total"))["p"] or 0

    recent_transactions = Transaction.objects.select_related(
        "reseller", "product"
    ).order_by("-created_at")[:10]

    low_stock = Product.objects.filter(stock__lt=100)

    context = {
        "total_stock": total_stock,
        "total_resellers": total_resellers,
        "total_credit": total_credit,
        "revenue_today": revenue_today,
        "revenue_week": revenue_week,
        "pending_payments": pending_payments,
        "recent_transactions": recent_transactions,
        "low_stock": low_stock,
        "today": today,
    }
    return render(request, "dashboard.html", context)


def stock_list(request):
    products = Product.objects.all()
    return render(request, "stock_list.html", {"products": products})


def reseller_list(request):
    resellers = Reseller.objects.all()
    return render(request, "reseller_list.html", {"resellers": resellers})

def inventory_command_center(request):
    today = date.today()
    products = Product.objects.all().order_by('stock')
    movements = StockMovement.objects.select_related('product', 'reseller').order_by('-created_at')[:50]
    
    total_stock = Product.objects.aggregate(s=Sum("stock"))["s"] or 0
    total_receivables = Reseller.objects.aggregate(c=Sum("credit"))["c"] or 0
    today_sales = Transaction.objects.filter(created_at__date=today).aggregate(s=Sum("total"))["s"] or 0

    context = {
        "products": products,
        "movements": movements,
        "total_stock": total_stock,
        "total_receivables": total_receivables,
        "today_sales": today_sales,
    }
    return render(request, "inventory.html", context)

@csrf_exempt
def telegram_webhook(request, token):
    if token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponse("Unauthorized", status=401)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            
            parsed = parse_message(text)
            
            if "error" in parsed:
                reply = f"❌ Format salah.\n\nContoh format:\nJUAL [produk] [qty] bks [reseller]\nCONTOH [produk] [qty] bks [reseller]\nRETUR [produk] [qty] bks [reseller]\nSTOK [produk]\nPIUTANG [reseller]"
            else:
                action = parsed.get("action")
                if action == "JUAL":
                    reply = commands.process_sales(
                        parsed["product"], 
                        parsed["qty"], 
                        parsed["reseller"], 
                        parsed.get("price")
                    )
                elif action == "CONTOH":
                    reply = commands.process_sample(
                        parsed["product"], 
                        parsed["qty"], 
                        parsed["reseller"]
                    )
                elif action == "RETUR":
                    reply = commands.process_return(
                        parsed["product"], 
                        parsed["qty"], 
                        parsed["reseller"]
                    )
                elif action == "STOK":
                    reply = commands.get_stock(parsed.get("product"))
                elif action == "PIUTANG":
                    reply = commands.get_receivables(parsed.get("reseller"))
                else:
                    reply = "❓ Aksi tidak dikenal."
            
            send_telegram_message(chat_id, reply)
            
        return JsonResponse({"status": "ok"})
    
    return HttpResponse("Method not allowed", status=405)

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending telegram message: {e}")
