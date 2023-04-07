from django import forms
from django.core import  validators
from .models import Products

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows":5, "cols":30}),
#         validators=[validators.RegexValidator(
#             regex="great",
#             message="Field must contain word 'great'"
#         )]
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = "name", "price", "description", "discount"