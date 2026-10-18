from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Product, Reseller, Transaction, StockMovement


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