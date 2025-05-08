from django.db import models
from django.contrib.auth.models import AbstractUser


#from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    user_name = models.CharField(max_length=128, null=True, blank=True,verbose_name='ユーザー名')
    hurigana = models.CharField(max_length=128, null=True, blank=True,verbose_name='フリガナ')
    zip_code = models.CharField(max_length=16, null=True, blank=True,verbose_name='郵便番号')
    address = models.CharField(max_length=255, null=True, blank=True,verbose_name='住所')
    phone_number = models.CharField(max_length=20, null=True, blank=True,verbose_name='電話番号')
    birthday = models.DateField(null=True, blank=True,verbose_name='誕生日')
    job = models.CharField(max_length=255, null=True, blank=True,verbose_name='職業')
    is_subscribed = models.BooleanField(default=False, verbose_name='有料会員')
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True,verbose_name='StripeカスタマーID')
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True,verbose_name='StripeサブスクリプションID')
    stripe_card_last4 = models.CharField(max_length=10, null=True, blank=True,verbose_name='Stripeカード下４桁')
    stripe_card_brand = models.CharField(max_length=20, null=True, blank=True,verbose_name='Stripeカードブランド')
    stripe_card_exp_month = models.IntegerField(default=0, verbose_name='Stripeカード有効月')
    stripe_card_exp_year = models.IntegerField(default=0, verbose_name='Stripeカード有効年')

    class Meta:
        verbose_name_plural = 'CustomUser'

        def __str__(self):
            return self.username