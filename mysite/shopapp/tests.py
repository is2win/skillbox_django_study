from django.contrib.auth.models import User
from django.test import TestCase

from mysite import settings
from shopapp.utils import add_two_numbers
from django.urls import reverse
from string import ascii_letters
from random import choices
from shopapp.models import Products

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(5, 6)
        self.assertEqual(result, 11)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.products_name = "".join(choices(ascii_letters, k=10))
        Products.objects.filter(name=self.products_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:products_creat"),
            {
                "name": self.products_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Products.objects.filter(name=self.products_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Products.objects.create(name="Beast Product")


    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
    # def setUp(self) -> None:
    #     # выполняем перед тестом
    #     self.product = Products.objects.create(name="Beast Product")
    #
    # def tearDown(self) -> None:
    #     # выполняем после теста, даже если тест провалится
    #     self.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_links(self):
        response = self.client.get(
            reverse("shopapp:products_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestVase(TestCase):
    fixtures = [
        'products-fixture.json'
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        # products = Products.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        # второй вариант проверки
        self.assertQuerysetEqual(
            qs=Products.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products_list.html')



class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bib", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Products.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )