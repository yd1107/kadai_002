# Generated by Django 4.2 on 2024-12-02 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0, verbose_name='年間売上')),
                ('month', models.IntegerField(default=0, verbose_name='月間売上')),
                ('amount', models.IntegerField(default=0, verbose_name='売上金額')),
            ],
        ),
    ]