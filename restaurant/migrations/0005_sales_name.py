# Generated by Django 4.2 on 2024-12-02 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_sales_month_alter_sales_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='売上'),
        ),
    ]
