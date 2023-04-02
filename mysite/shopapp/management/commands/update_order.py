from django.core.management import BaseCommand

from shopapp.models import Order, Products


class Command(BaseCommand):
    def handle(self, *args, **options):
            order = Order.objects.first()
            if not order:
                self.stdout.write("no order found")
                return
            products = Products.objects.all()
            for product in products:
                order.products.add(product)
            order.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully added products {order.products.all()} to order {order}"
                )
            )