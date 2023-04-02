from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .admin_mixins import ExportAsCSVMixin
# Register your models here.
from .models import Products, Order


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

class OrderInline(admin.TabularInline):
    model = Products.orders.through

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    # list_display = "pk", "name", "description", "price", "discount"
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for delete"
        })
    ]
    def description_short(self, obj: Products):
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

# admin.site.register(Products, ProductsAdmin)

# class ProductsInline(admin.TabularInline):
class ProductsInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductsInline,
    ]
    list_display = "delivery_adress", "promocode", "created_at", "user_verbose"
    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username