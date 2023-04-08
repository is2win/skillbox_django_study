from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductsListView,
    products_list,
    ProductCreateView,
    OrdersListView,
    OrderDetailView,
    ProductUpdateView,
    ProductDeleteView,
    create_product
)

app_name = 'shopapp'

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="group_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create", ProductCreateView.as_view(), name="products_creat"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/confirm-delete/", ProductDeleteView.as_view(), name="products_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders_detail_view"),
    path("products/create", create_product, name="product_create"),
]