# Generated by Django 4.2 on 2024-11-04 14:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='カテゴリー名')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='写真')),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='店舗名')),
                ('description', models.CharField(max_length=128, verbose_name='説明')),
                ('price', models.CharField(max_length=32, verbose_name='価格帯')),
                ('zip_code', models.CharField(max_length=32, verbose_name='郵便番号')),
                ('address', models.CharField(max_length=128, verbose_name='住所')),
                ('business_time', models.CharField(max_length=64, verbose_name='営業時間')),
                ('close_day_of_week', models.CharField(max_length=32, verbose_name='定休日')),
                ('seats_number', models.CharField(max_length=32, verbose_name='座席数')),
                ('rate', models.FloatField(default=0.0, verbose_name='レート')),
                ('review_num', models.IntegerField(default=0, verbose_name='レビュー数')),
                ('reservation_num', models.IntegerField(default=0, verbose_name='予約数')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='写真')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.category', verbose_name='カテゴリー')),
            ],
            options={
                'verbose_name_plural': 'Restaurant',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5, verbose_name='レート')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='コメント')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='レビュー作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='レビュー更新日時')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.restaurant', verbose_name='レストラン')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='予約日')),
                ('time', models.TimeField(choices=[('', '選択してください'), (datetime.time(2, 3), '2:30'), (datetime.time(3, 0), '3:00'), (datetime.time(3, 30), '3:30'), (datetime.time(4, 0), '4:00'), (datetime.time(4, 30), '4:30'), (datetime.time(5, 0), '5:00'), (datetime.time(5, 30), '5:30'), (datetime.time(6, 0), '6:00'), (datetime.time(6, 30), '6:30'), (datetime.time(7, 0), '7:00'), (datetime.time(7, 30), '7:30'), (datetime.time(8, 0), '8:00'), (datetime.time(8, 30), '8:30'), (datetime.time(9, 0), '9:00'), (datetime.time(9, 30), '9:30'), (datetime.time(10, 0), '10:00'), (datetime.time(10, 30), '10:30')], default='', verbose_name='時間')),
                ('number_of_people', models.IntegerField(choices=[('', '選択してください'), (1, '1名'), (2, '2名'), (3, '3名'), (4, '4名'), (5, '5名'), (6, '6名'), (7, '7名'), (8, '8名'), (9, '9名'), (10, '10名'), (11, '11名'), (12, '12名'), (13, '13名'), (14, '14名'), (15, '15名'), (16, '16名'), (17, '17名'), (18, '18名'), (19, '19名'), (20, '20名'), (21, '21名'), (22, '22名'), (23, '23名'), (24, '24名'), (25, '25名'), (26, '26名'), (27, '27名'), (28, '28名'), (29, '29名'), (30, '30名'), (31, '31名'), (32, '32名'), (33, '33名'), (34, '34名'), (35, '35名'), (36, '36名'), (37, '37名'), (38, '38名'), (39, '39名'), (40, '40名'), (41, '41名'), (42, '42名'), (43, '43名'), (44, '44名'), (45, '45名'), (46, '46名'), (47, '47名'), (48, '48名'), (49, '49名'), (50, '50名')], default='', verbose_name='人数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='予約申し込み日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='予約更新日時')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.restaurant', verbose_name='レストラン')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Reservation',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='お気に入り登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='お気に入り更新日時')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.restaurant', verbose_name='レストラン')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Favorite',
            },
        ),
    ]
