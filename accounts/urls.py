from django.urls import path
from . import views



urlpatterns = [
  path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
  path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
  path("subscribe-register/", views.SubscribeRegisterView.as_view(),name="subscribe_register"),
  path("subscribe-cancel/", views.SubscribeCancelView.as_view(),name="subscribe_cancel"),
  path("subscribe-payment/", views.SubscribePaymentView.as_view(),name="subscribe_payment"),
  path("management/user-list",views.ManagementUserListView.as_view(), name="user_list"),
  path("management/user-list-update/<int:pk>/",views.ManagementUserUpdateView.as_view(), name="user_list_update"),
  path("management/restaurant-list",views.ManagementRestaurantListView.as_view(), name="restaurant_list"),
  path("management/restaurant-create/",views.ManagementRestaurantCreateView.as_view(), name="restaurant_create"),
  path("management/category-list",views.ManagementCategoryListView.as_view(), name="category_list"),
  path("management/category-list-update/<int:pk>/",views.ManagementCategoryUpdateView.as_view(), name="category_list_update"),
]