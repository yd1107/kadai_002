# Generated by Django 4.2 on 2024-12-20 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_remove_restaurant_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='name',
        ),
    ]
