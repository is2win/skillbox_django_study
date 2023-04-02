from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="romai")
        order = Order.objects.get_or_create(
            delivery_adress="Some street, d8",
            promocode="sale12",
            user=user,
        )
        self.stdout.write(f"created order {order}")
