# Generated by Django 4.2.5 on 2024-02-06 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='avatar.png', upload_to='User_images'),
        ),
    ]
