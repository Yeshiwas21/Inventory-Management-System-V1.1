from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    serial = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=200)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='added_products')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'

class Request(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    requested_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='requested_by')
    additional_info = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    status_choices = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    storekeeper_approval_status = models.CharField(max_length=10, choices=status_choices, default='pending')
    admin_approval_status = models.CharField(max_length=10, choices=status_choices, default='pending')
    storekeeper_approved_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='stokeeper_approved_by')
    admin_approved_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='admin_approved_by')
    storekeeper_approved_date = models.DateTimeField(null=True)
    admin_approved_date = models.DateTimeField(null=True)
    assignet_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='assignet_to', null=True)
