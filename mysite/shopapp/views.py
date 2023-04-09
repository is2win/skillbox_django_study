from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from.forms import ProductForm
from .models import Products, Order
from .forms_2 import GroupForm
from django.views import View


class ProductDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy("shopapp:products_list")

    # soft delete - архивирование и оставляем в базе
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    # full delete
    # class ProductDeleteView(DeleteView):
    # model = Products
    # success_url = reverse_lazy("shopapp:products_list")



# class ProductCreateView(UserPassesTestMixin, CreateView):
class ProductCreateView(CreateView):
    def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        return self.request.user.is_superuser
    model = Products
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Products
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:products_details",
            kwargs={"pk": self.object.pk}
        )

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
        }
        return render(request, 'shopapp/shop_index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailView(DetailView):
    template_name = "shopapp/products-details.html"
    model = Products
    context_object_name = "product"
    # def get(self, request: HttpRequest, pk: int) -> HttpResponse:
    #     product = get_object_or_404(Products, pk=pk)
    #     context = {
    #         "product": product,
    #     }
    #     return render(request, "shopapp/products-details.html", context=context)


class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    model = Products
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["products"] = Products.objects.all()
    #     return context
    context_object_name = "products"
    queryset = Products.objects.filter(archived=False)


def products_list(request: HttpRequest):
    context = {
        "products": Products.objects.all(),
    }
    return render(request, 'shopapp/products_list.html', context=context)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products"))


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products"))


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all()
#     }
#     return render(request, 'shopapp/orders_list.html', context=context)





def create_product(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            # price = form.cleaned_data["price"]
            # Products.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }

    return render(request, "shopapp/create-product.html", context=context)


class ProductsDataExcportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Products.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})