from django.contrib import admin
from .models import Product, Category
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
