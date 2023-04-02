from django.core.management import BaseCommand
from shopapp.models import Products


class Command(BaseCommand):
    """
    Creates products
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")
        products = [
            "Laptop",
            "Desktop",
            "Smartphone",
        ]
        for product_name in products:
            product, created = Products.objects.get_or_create(name=product_name)
            self.stdout.write(f"created product {product.name}")
        self.stdout.write(self.style.SUCCESS("Product created"))