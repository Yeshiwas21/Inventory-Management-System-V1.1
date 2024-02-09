from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('storekeeper', 'Store Keeper'),
        ('admin', 'Admin'),
    ]
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')
    phone = models.CharField(max_length=14, default='123456789')
    email = models.EmailField()
    image = models.ImageField(default='avatar.png', upload_to='User_images', blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)

    # Add unique related_name arguments to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )



class Storekeeper(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
