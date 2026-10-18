from django.contrib import admin
from .models import Product, Reseller, StockMovement, Transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "price_buy", "price_sell", "margin_per_unit", "stock", "created_at"]
    search_fields = ["name", "sku"]
    list_filter = ["created_at"]

@admin.register(Reseller)
class ResellerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "tier", "credit", "active", "total_transactions", "created_at"]
    search_fields = ["name", "phone"]
    list_filter = ["tier", "active"]

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["product", "reseller", "movement_type", "quantity", "created_at"]
    search_fields = ["product__name", "reseller__name"]
    list_filter = ["movement_type", "created_at"]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["reseller", "product", "quantity", "price_per_unit", "total", "payment_status", "created_at"]
    search_fields = ["reseller__name", "product__name"]
    list_filter = ["payment_status", "created_at"]