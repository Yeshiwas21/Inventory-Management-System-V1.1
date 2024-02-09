from django import forms
from .models import Product, Category, Request


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'serial', 'category','description', 'price', 'quantity', 'unit']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:  # Changed condition to check if quantity is less than 1
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class RequestProductForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['quantity', 'additional_info']

    request_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a at least 1.")
        return quantity
