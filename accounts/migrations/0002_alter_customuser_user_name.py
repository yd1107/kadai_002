# Generated by Django 4.2 on 2024-12-02 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='ユーザー名'),
        ),
    ]