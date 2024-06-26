# Generated by Django 4.2.5 on 2024-02-02 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0006_alter_request_admin_approved_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='admin_approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='request',
            name='storekeeper_approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stokeeper_approved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
