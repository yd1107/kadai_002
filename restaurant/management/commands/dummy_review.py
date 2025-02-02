from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser
from restaurant.models import Restaurant, Review
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from faker import Faker


class Command(BaseCommand):
    help = "評価ダミー生成"

    @transaction.atomic()
    def handle(self, *args, **options):
      print("評価ダミー生成")

      fake = Faker("ja-JP")

      users = CustomUser.objects.all()
      restaurants = Restaurant.objects.all()

      for restaurant in restaurants:
          for user in users:
              #　レビュー数をランダムに設定
              review_count = int(round(np.random.normal(loc=0.2, scale=0.3)))

              # レビュー数が0以上の場合。レビューを生成
              if review_count > 0:
                  for _ in range(review_count):
                   #評価してデータをランダムに生成
                        x = np.random.normal(loc=3.5, scale=0.8)
                        rating_value = 1 if x < 1 else 5 if x > 5 else Decimal(str(x)).quantize(Decimal('0'), ROUND_HALF_UP)

                        if np.random.normal() <  0.5:
                            comment = fake.text()
                        else:
                          comment = ""

                        Review.objects.create(
                            restaurant = restaurant,
                            user = user,
                            rate = rating_value,
                            comment = comment
                        )