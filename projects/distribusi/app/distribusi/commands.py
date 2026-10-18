from django.db import transaction as db_transaction
from django.db.models import Sum
from .models import Product, Reseller, StockMovement, Transaction

def fuzzy_find_product(name):
    if not name: return None
    # Try exact match first
    product = Product.objects.filter(name__iexact=name).first()
    if not product:
        # Try partial match
        product = Product.objects.filter(name__icontains=name).first()
    return product

def fuzzy_find_reseller(name):
    if not name: return None
    reseller = Reseller.objects.filter(name__iexact=name).first()
    if not reseller:
        reseller = Reseller.objects.filter(name__icontains=name).first()
    return reseller

def process_sales(product_name, qty, reseller_name, price=None):
    product = fuzzy_find_product(product_name)
    if not product:
        return f"❌ Produk '{product_name}' tidak ditemukan."
    
    reseller = fuzzy_find_reseller(reseller_name)
    if not reseller:
        return f"❌ Reseller '{reseller_name}' tidak ditemukan."
    
    if product.stock < qty:
        return f"❌ Stok tidak mencukupi. Stok {product.name}: {product.stock} bks."

    sell_price = price if price is not None else product.price_sell
    total_price = qty * sell_price

    with db_transaction.atomic():
        # Create Transaction
        Transaction.objects.create(
            reseller=reseller,
            product=product,
            quantity=qty,
            price_per_unit=sell_price,
            total=total_price,
            payment_status='unpaid'
        )
        
        # Create Stock Movement
        StockMovement.objects.create(
            product=product,
            reseller=reseller,
            movement_type='out',
            quantity=qty,
            notes=f"Penjualan ke {reseller.name}"
        )
        
        # Update Product Stock
        product.stock -= qty
        product.save()
        
        # Update Reseller Credit
        reseller.credit += total_price
        reseller.save()

    return f"✅ Penjualan berhasil: {product.name} x{qty} bks ke {reseller.name} (Total: Rp {total_price:,})."

def process_sample(product_name, qty, reseller_name):
    product = fuzzy_find_product(product_name)
    if not product:
        return f"❌ Produk '{product_name}' tidak ditemukan."
    
    reseller = fuzzy_find_reseller(reseller_name)
    if not reseller:
        return f"❌ Reseller '{reseller_name}' tidak ditemukan."
    
    if product.stock < qty:
        return f"❌ Stok tidak mencukupi untuk sample. Stok {product.name}: {product.stock} bks."

    with db_transaction.atomic():
        StockMovement.objects.create(
            product=product,
            reseller=reseller,
            movement_type='sample',
            quantity=qty,
            notes=f"Sample untuk {reseller.name}"
        )
        product.stock -= qty
        product.save()

    return f"✅ Sample berhasil: {product.name} x{qty} bks untuk {reseller.name}."

def process_return(product_name, qty, reseller_name):
    product = fuzzy_find_product(product_name)
    if not product:
        return f"❌ Produk '{product_name}' tidak ditemukan."
    
    reseller = fuzzy_find_reseller(reseller_name)
    if not reseller:
        return f"❌ Reseller '{reseller_name}' tidak ditemukan."

    with db_transaction.atomic():
        StockMovement.objects.create(
            product=product,
            reseller=reseller,
            movement_type='return',
            quantity=qty,
            notes=f"Retur dari {reseller.name}"
        )
        product.stock += qty
        product.save()

    return f"✅ Retur berhasil: {product.name} x{qty} bks dari {reseller.name}."

def get_stock(product_name=None):
    if product_name:
        product = fuzzy_find_product(product_name)
        if not product:
            return f"❌ Produk '{product_name}' tidak ditemukan."
        return f"📦 Stok {product.name}: {product.stock} bks."
    
    products = Product.objects.all()
    if not products:
        return "📦 Belum ada produk."
    
    lines = ["📦 Status Stok:"]
    for p in products:
        status = "🔴" if p.stock < 50 else "🟢"
        lines.append(f"- {status} {p.name}: {p.stock} bks")
    return "\n".join(lines)

def get_receivables(reseller_name=None):
    if reseller_name:
        reseller = fuzzy_find_reseller(reseller_name)
        if not reseller:
            return f"❌ Reseller '{reseller_name}' tidak ditemukan."
        return f"💸 Piutang {reseller.name}: Rp {reseller.credit:,}"
    
    resellers = Reseller.objects.filter(credit__gt=0)
    if not resellers:
        return "💸 Tidak ada piutang saat ini."
    
    lines = ["💸 Daftar Piutang:"]
    total_all = 0
    for r in resellers:
        lines.append(f"- {r.name}: Rp {r.credit:,}")
        total_all += r.credit
    lines.append(f"\nTotal Semua: Rp {total_all:,}")
    return "\n".join(lines)
