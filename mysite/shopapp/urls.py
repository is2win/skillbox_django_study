from django.urls import path
from .views import shop_index, group_list, products_list, orders_list

app_name = 'shopapp'

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", group_list, name="group_list"),
    path("products/", products_list, name="products_list"),
    path("orders/", orders_list, name="orders_list"),
]