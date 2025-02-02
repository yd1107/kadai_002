from django.contrib import admin

from django.contrib import admin
from .models import Category, Restaurant, Reservation, Review, Favorite, Sales

class ReviewAdmin(admin.ModelAdmin):
      list_display = ("id", "user", "restaurant","rate", "comment")
      search_fields = ("user",)

class FavoriteAdmin(admin.ModelAdmin):
      list_display = ("id", "user", "restaurant")
      search_fields = ("user",)


admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Sales)
