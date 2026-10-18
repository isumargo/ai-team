import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from distribusi.models import Product, Reseller, Transaction, StockMovement
from django.db import transaction as db_transaction

class Command(BaseCommand):
    help = 'Generates 7 days of realistic transaction data'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=7, help='Number of days to seed')

    def handle(self, *args, **options):
        days = options['days']
        products = list(Product.objects.all())
        resellers = list(Reseller.objects.all())

        if not products or not resellers:
            self.stdout.write(self.style.ERROR('Products or Resellers missing. Please ensure they exist.'))
            return

        self.stdout.write(f'Seeding data for the last {days} days...')

        # Clear existing transactions/movements to start fresh for seeding? 
        # The prompt says "Seed data management command for 7 days", but doesn't say clear.
        # I'll just add to existing.

        start_date = timezone.now() - timedelta(days=days)
        
        # Reset stocks to a healthy level first for demo
        for p in products:
            p.stock = 1000
            p.save()
        
        # Reset reseller credit
        for r in resellers:
            r.credit = 0
            r.save()

        count_transactions = 0
        count_movements = 0

        for day in range(days + 1):
            current_day = start_date + timedelta(days=day)
            
            # Number of transactions per day (3-8)
            num_tx = random.randint(3, 8)
            
            for _ in range(num_tx):
                # Random time during the day
                timestamp = current_day.replace(
                    hour=random.randint(8, 17),
                    minute=random.randint(0, 59)
                )
                
                reseller = random.choice(resellers)
                product = random.choice(products)
                qty = random.randint(10, 100)
                
                # Determine action type
                roll = random.random()
                if roll < 0.7: # 70% Sale
                    with db_transaction.atomic():
                        price = product.price_sell
                        total = qty * price
                        
                        tx = Transaction.objects.create(
                            reseller=reseller,
                            product=product,
                            quantity=qty,
                            price_per_unit=price,
                            total=total,
                            payment_status=random.choice(['paid', 'unpaid', 'partial']),
                            notes='Generated seed data'
                        )
                        tx.created_at = timestamp
                        tx.save()
                        
                        sm = StockMovement.objects.create(
                            product=product,
                            reseller=reseller,
                            movement_type='out',
                            quantity=qty,
                            notes='Generated sale'
                        )
                        sm.created_at = timestamp
                        sm.save()
                        
                        product.stock -= qty
                        product.save()
                        
                        if tx.payment_status != 'paid':
                            reseller.credit += total
                            reseller.save()
                        
                        count_transactions += 1
                        count_movements += 1
                        
                elif roll < 0.85: # 15% Sample
                    with db_transaction.atomic():
                        sm = StockMovement.objects.create(
                            product=product,
                            reseller=reseller,
                            movement_type='sample',
                            quantity=random.randint(1, 5),
                            notes='Generated sample'
                        )
                        sm.created_at = timestamp
                        sm.save()
                        
                        product.stock -= sm.quantity
                        product.save()
                        count_movements += 1
                        
                else: # 15% Return
                    with db_transaction.atomic():
                        sm = StockMovement.objects.create(
                            product=product,
                            reseller=reseller,
                            movement_type='return',
                            quantity=random.randint(5, 20),
                            notes='Generated return'
                        )
                        sm.created_at = timestamp
                        sm.save()
                        
                        product.stock += sm.quantity
                        product.save()
                        count_movements += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count_transactions} transactions and {count_movements} movements.'))
