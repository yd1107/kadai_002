from django.shortcuts import render , redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic , View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
import stripe

from . import forms
from . import models
from .mixins import onlyMnagementUserMixin

from .models import CustomUser
from restaurant.models import Category
from restaurant.models import Restaurant
from restaurant.models import Sales
import nagoyameshi.settings as settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.CustomUser
    template_name = 'user/user_detail.html'
    

class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.CustomUser
    template_name = 'user/user_update.html'
    form_class = forms.UserUpdateForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('user_detail', kwargs={'pk': pk})

    def form_valid(self, form):
        return super().form_valid(form)
      
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = get_object_or_404(CustomUser, id=pk)

        context["user"] = user

        return context
    
class SubscribeRegisterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # YOUR_DOMAINが開発環境と本番環境で変わるようにsettings.pyに記述
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1RCiz2R3SnzpPnG31qWHEGnz',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{settings.YOUR_DOMAIN}/accounts/subscribe-success/?session_id={{CHECKOUT_SESSION_ID}}&user_id={request.user.id}",
            cancel_url=f"{settings.YOUR_DOMAIN}/accounts/subscribe-register/",
        )   
        return redirect(checkout_session.url, code=303)
    
    def get(self, request, *args, **kwargs):    
        return render(request, 'subscribe/subscribe_register.html')
    
class SubscribeSuccessView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):    
        session_id = request.GET.get('session_id')
        user_id = request.GET.get('user_id')

        if not session_id or not user_id:
            return HttpResponse("Invalid request", status=400)

        # ユーザーの subscription 項目を更新
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_subscribed = True
        user.save()
        
        return redirect(reverse_lazy('top_page'))




class SubscribeCancelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'subscribe/subscribe_cancel.html'
    
    def post(self, request):
        user_id = request.user.id
        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=False)
        return redirect(reverse_lazy('top_page'))



#ここから管理者側

#ユーザーリスト
class ManagementUserListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/user_list.html"
    model = models.CustomUser
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "user"
        
        return context


class ManagementUserUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    template_name = 'management/user_list_update.html'
    form_class =forms.UserUpdateForm
    model = models.CustomUser
    success_url = reverse_lazy('user_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_user_id"] = self.request.path.split('/')[-2]
        context["selected"] = "user"
        
        return context
    

class ManagementUserDeleteView(onlyMnagementUserMixin, generic.DeleteView):
    model = models.CustomUser
    template_name = 'management/user_list_delete.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del_user_id = self.request.path.split('/')[-2]
        context["del_user"] = models.CustomUser.objects.get(id=del_user_id)
        context["selected"] = "user"

        return context

    


#カテゴリー
class ManagementCategoryListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/category_list.html"
    model = Category
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "category"
        
        return context


class ManagementCategoryCreateView(onlyMnagementUserMixin, generic.CreateView):
    model = Category
    form_class = forms.CategoryCreateForm
    template_name = 'management/category_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "category"
        
        return context


class ManagementCategoryUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    model = Category
    form_class = forms.CategoryUpdateForm
    template_name = 'management/category_update.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_category_id"] = self.request.path.split('/')[-2]
        context["selected"] = "category"

        return context

class ManagementCategoryDeleteView(onlyMnagementUserMixin, generic.DeleteView):
    model = Category
    fields = '__all__'
    template_name = 'management/category_delete.html'  
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del_category_id = self.request.path.split('/')[-2]
        context["del_category"] = Category.objects.get(id=del_category_id)
        context["selected"] = "category"

        return context

#店舗
class ManagementRestaurantCreateView(onlyMnagementUserMixin, generic.CreateView):
    model = Restaurant
    template_name = 'management/restaurant_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "restaurant"
        
        return context

class ManagementRestaurantListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/restaurant_manage_list.html"
    model = Restaurant
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "restaurant"
        
        return context

class ManagementRestaurantUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    template_name = 'management/restaurant_update.html'
    form_class = forms.RestaurantUpdateForm
    model = Restaurant
    success_url = reverse_lazy('restaurant_manage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_restaurant_id"] = self.request.path.split('/')[-2]
        context["selected"] = "restaurant"

        return context

class ManagementRestaurantDeleteView(onlyMnagementUserMixin, generic.DeleteView):
    model = Restaurant
    template_name = 'management/restaurant_delete.html'
    success_url = reverse_lazy('restaurant_manage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del_restaurant_id = self.request.path.split('/')[-2]
        context["del_restaurant"] = Restaurant.objects.get(id=del_restaurant_id)
        context["selected"] = "restaurant"

        return context


#売上
class ManagementSalesListView(onlyMnagementUserMixin, generic.ListView):
    template_name = 'management/sales.html'
    model = Sales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "sales"
        
        return context



