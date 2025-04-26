from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser

class Command(BaseCommand):
  def handle(self, *args, **options):
    fake = Faker("ja-JP")
    users = CustomUser.objects.all()
    
    for user in users:
      birthday = fake.date_of_birth(minimum_age=18, maximum_age=70)
      user.birthday = birthday
      user.save()
    