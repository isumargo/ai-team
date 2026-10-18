from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price_buy = models.DecimalField(max_digits=12, decimal_places=0, default=7600, help_text="Modal per bungkus")
    price_sell = models.DecimalField(max_digits=12, decimal_places=0, default=8600, help_text="Harga jual ke reseller")
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Stok: {self.stock})"

    @property
    def margin_per_unit(self):
        return self.price_sell - self.price_buy


class Reseller(models.Model):
    TIER_CHOICES = [
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="bronze")
    credit = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text="Total piutang")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-active", "name"]

    def __str__(self):
        return self.name

    @property
    def total_transactions(self):
        return self.transaction_set.count()


class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ("in", "Barang Masuk"),
        ("out", "Barang Keluar"),
        ("sample", "Sample"),
        ("return", "Retur"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reseller = models.ForeignKey(Reseller, on_delete=models.SET_NULL, null=True, blank=True)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_CHOICES)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_movement_type_display()} — {self.product.name} x{self.quantity}"


class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ("paid", "Lunas"),
        ("unpaid", "Belum Bayar"),
        ("partial", "Cicilan"),
    ]
    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=0)
    total = models.DecimalField(max_digits=14, decimal_places=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="unpaid")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reseller.name} — {self.product.name} x{self.quantity} ({self.get_payment_status_display()})"

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)