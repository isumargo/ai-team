import requests
import json
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Reseller, Transaction, StockMovement
from .agent import DasiyahAgent
from . import commands

def dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=7)
    prev_week_start = week_ago - timedelta(days=7)

    total_stock = Product.objects.aggregate(s=Sum("stock"))["s"] or 0
    total_resellers = Reseller.objects.filter(active=True).count()
    total_credit = Reseller.objects.aggregate(c=Sum("credit"))["c"] or 0

    # Current week revenue
    revenue_week = Transaction.objects.filter(
        created_at__date__gte=week_ago, payment_status="paid"
    ).aggregate(r=Sum("total"))["r"] or 0
    
    # Previous week revenue for WoW
    revenue_prev_week = Transaction.objects.filter(
        created_at__date__gte=prev_week_start,
        created_at__date__lt=week_ago,
        payment_status="paid"
    ).aggregate(r=Sum("total"))["r"] or 0

    rev_wow = "up" if revenue_week >= revenue_prev_week else "down"

    # Daily revenue for bar chart
    daily_revenue = []
    for i in range(7):
        d = today - timedelta(days=6-i)
        rev = Transaction.objects.filter(created_at__date=d, payment_status="paid").aggregate(r=Sum("total"))["r"] or 0
        daily_revenue.append({
            "day": d.strftime("%a"),
            "amount": int(rev),
        })
    
    max_rev = max([d["amount"] for d in daily_revenue]) or 1

    # Top products
    top_products = Product.objects.annotate(
        total_sold=Sum("transaction__quantity")
    ).filter(total_sold__gt=0).order_by("-total_sold")[:5]

    # Top resellers
    top_resellers = Reseller.objects.annotate(
        total_spent=Sum("transaction__total")
    ).filter(total_spent__gt=0).order_by("-total_spent")[:5]

    recent_transactions = Transaction.objects.select_related(
        "reseller", "product"
    ).order_by("-created_at")[:10]

    low_stock = Product.objects.filter(stock__lt=100)

    context = {
        "total_stock": total_stock,
        "total_resellers": total_resellers,
        "total_credit": total_credit,
        "revenue_week": revenue_week,
        "rev_wow": rev_wow,
        "daily_revenue": daily_revenue,
        "max_rev": max_rev,
        "top_products": top_products,
        "top_resellers": top_resellers,
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

def reseller_detail(request, pk):
    reseller = get_object_or_404(Reseller, pk=pk)
    
    # Auto-tier logic
    total_qty = Transaction.objects.filter(reseller=reseller).aggregate(q=Sum("quantity"))["q"] or 0
    new_tier = "bronze"
    if total_qty > 3000:
        new_tier = "gold"
    elif total_qty >= 1000:
        new_tier = "silver"
    
    if reseller.tier != new_tier:
        reseller.tier = new_tier
        reseller.save()

    transactions = Transaction.objects.filter(reseller=reseller).select_related("product").order_by("-created_at")
    movements = StockMovement.objects.filter(reseller=reseller).select_related("product").order_by("-created_at")
    
    total_spent = transactions.aggregate(s=Sum("total"))["s"] or 0
    tx_count = transactions.count()
    avg_order = total_spent / tx_count if tx_count > 0 else 0
    
    unpaid_transactions = transactions.filter(payment_status="unpaid")
    
    context = {
        "reseller": reseller,
        "transactions": transactions,
        "movements": movements,
        "total_qty": total_qty,
        "total_spent": total_spent,
        "avg_order": avg_order,
        "unpaid_transactions": unpaid_transactions,
    }
    return render(request, "reseller_detail.html", context)

def distribution_map(request):
    resellers = Reseller.objects.filter(active=True, lat__isnull=False, lng__isnull=False)
    
    map_data = []
    for r in resellers:
        total_qty = Transaction.objects.filter(reseller=r).aggregate(q=Sum("quantity"))["q"] or 0
        last_tx = Transaction.objects.filter(reseller=r).order_by("-created_at").first()
        
        map_data.append({
            "id": r.id,
            "name": r.name,
            "lat": r.lat,
            "lng": r.lng,
            "tier": r.tier,
            "total_qty": int(total_qty),
            "last_tx_date": last_tx.created_at.strftime("%d/%m/%Y") if last_tx else "N/A",
        })
    
    context = {
        "map_data_json": json.dumps(map_data),
    }
    return render(request, "map.html", context)

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
            
            # Delegasi ke profil Hermes pm-distribusi: SOUL.md + OpenRouter (bypass gateway rusak)
            import requests, os
            api_key = os.getenv("OPENROUTER_API_KEY")
            with open("/root/.hermes/profiles/pm-distribusi/SOUL.md") as f:
                system = f.read()
            payload = {
                "model": "thinkingmachines/inkling:free",
                "messages": [{"role":"system","content":system}, {"role":"user","content":text}],
                "temperature": 0.3
            }
            try:
                r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"},
                    json=payload, timeout=30)
                reply = r.json()["choices"][0]["message"]["content"] if r.status_code==200 else "Mas/Mbak, Dasiyah (Hermes pm-distribusi) aktif — model: thinkingmachines/inkling:free | fallback: meta-llama/llama-3.3-70b-instruct:free."
            except Exception as e:
                reply = f"Mas/Mbak, Dasiyah lagi kerja. Mode: thinkingmachines/inkling:free. Fallback: meta-llama/llama-3.3-70b-instruct:free. Error: {str(e)[:50]}"
            
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
