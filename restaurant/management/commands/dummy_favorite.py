from random import randint
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser
from restaurant.models import Restaurant, Favorite


class Command(BaseCommand):
    help = "お気に入りダミー生成"

    @transaction.atomic()
    def handle(self, *args, **options):
      print("お気に入りダミー生成")

      users = CustomUser.objects.all()
      restaurants = Restaurant.objects.all()

      now = datetime.now()

      for user in users:
          for restaurant in restaurants:
              val = randint(0, 100)
              if val >= 85:
                  favorite = Favorite(
                    user = user,
                    restaurant = restaurant,
                    created_at = now,
                    updated_at = now
                  )

                  favorite.save()

