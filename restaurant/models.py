import datetime

from accounts.models import CustomUser
from django.db import models

#管理側ページ作成で追加
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    """カテゴリーモデル"""
    name = models.CharField(verbose_name='カテゴリー名', max_length=64)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    
    class Meta:
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'

    def __str__(self):
        return self.name

    # カテゴリの追加・編集完了時のリダイレクト先
    def get_absolute_url(self):
         return reverse('category_list')

class Restaurant(models.Model):
    """レストランモデル"""
    name = models.CharField(verbose_name='店舗名', max_length=64)
    description = models.CharField(verbose_name='説明', max_length=128)
    price_min = models.IntegerField(verbose_name="最低金額", default=1000)
    price_max = models.IntegerField(verbose_name="最高金額", default=5000)
    zip_code = models.CharField(verbose_name='郵便番号', max_length=32)
    address = models.CharField(verbose_name='住所', max_length=128)
    business_time = models.CharField(verbose_name='営業時間', max_length=64)
    open_time = models.TimeField(verbose_name="開店時間", default="17:00")
    close_time = models.TimeField(verbose_name="閉店時間", default="21:00")
    close_day_of_week = models.PositiveIntegerField(verbose_name='定休日', default=0)
    seats_number = models.CharField(verbose_name='座席数', max_length=32)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'レストラン'
        verbose_name_plural = 'レストラン'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant_list')

class Reservation(models.Model):
    """予約モデル"""   
    NUMBER_OF_PEOPLE = (
        ('','選択してください'), (1, '1名'), (2, '2名'), (3, '3名'), (4, '4名'),(5, '5名'), (6, '6名'), (7, '7名'),(8, '8名'), (9, '9名'), (10, '10名'),
        (11, '11名'), (12, '12名'), (13, '13名'), (14, '14名'), (15, '15名'),(16, '16名'), (17, '17名'), (18, '18名'),(19, '19名'), (20, '20名'),
        (21, '21名'), (22, '22名'), (23, '23名'), (24, '24名'), (25, '25名'),(26, '26名'), (27, '27名'), (28, '28名'),(29, '29名'), (30, '30名'),(31, '31名'), (32, '32名'), (33, '33名'), (34, '34名'), (35, '35名'),(36, '36名'), (37, '37名'), (38, '38名'),(39, '39名'), (40, '40名'),
        (41, '41名'), (42, '42名'), (43, '43名'), (44, '44名'), (45, '45名'),(46, '46名'), (47, '47名'), (48, '48名'),(49, '49名'), (50, '50名'),
        )

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name='レストラン', on_delete=models.PROTECT)
    date = models.DateField(verbose_name='予約日')
    time = models.TimeField(verbose_name='時間', default='')
    number_of_people = models.IntegerField(verbose_name='人数',choices=NUMBER_OF_PEOPLE, default='')
    created_at = models.DateTimeField(verbose_name='予約申し込み日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='予約更新日時', auto_now=True)

    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'

    def __str__(self):
        return self.restaurant.name


class Review(models.Model):
    """レビューモデル"""
    RATES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name='レストラン',on_delete=models.PROTECT)
    rate = models.IntegerField(verbose_name='レート', default=5, choices=RATES)
    comment = models.TextField(verbose_name='コメント', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='レビュー作成日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='レビュー更新日時',auto_now=True)
    
    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'
    def __str__(self):
        return self.restaurant.name

class Favorite(models.Model):
    """お気に入りモデル"""
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー',on_delete=models.PROTECT, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name='レストラン',on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='お気に入り登録日時',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='お気に入り更新日時',auto_now=True)
    
    class Meta:
        verbose_name= 'お気に入り'
        verbose_name_plural = 'お気に入り'
    def __str__(self):
        return self.restaurant.name

class Sales(models.Model):
    """売上モデル"""
    year = models.IntegerField('年', default=0)
    month = models.IntegerField('月', default=0)
    amount = models.IntegerField('売上金額', default=0)

    class Meta:
        verbose_name = '売上'
        verbose_name_plural = '売上'

    def __str__(self):
        return self.name
