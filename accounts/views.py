from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views import generic , View
from django.views.generic.edit import CreateView

from . import forms
from . import models
from .mixins import onlyMnagementUserMixin

from restaurant.models import Category
from restaurant.models import Restaurant
from restaurant.models import Sales


# Create your views here.
class UserDetailView(generic.DetailView):
    model = models.CustomUser
    template_name = 'user/user_detail.html'
    

class UserUpdateView(generic.UpdateView):
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

class SubscribeRegisterView(View):
    template = 'subscribe/subscribe_register.html'
    def get(self, request):
      context = {}
      return render(self.request, self.template, context)

    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')

        correct_cord_number = '4242424242424242'
        if card_number != correct_cord_number:
            context = {
                'error_message': 'クレジットカード番号が正しくありません'
                }
            return render(self.request, self.template, context)
        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=True,card_name=card_name,card_number=card_number)
        return redirect(reverse_lazy('top_page'))

class SubscribeCancelView(generic.TemplateView):
    template_name = 'subscribe/subscribe_cancel.html'
    def post(self, request):
        user_id = request.user.id
        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=False)
        return redirect(reverse_lazy('top_view'))

class SubscribePaymentView(View):
    template = 'subscribe/subscribe_payment.html'

    def get(self, request):
        user_id = request.user.id
        user = models.CustomUser.objects.get(id=user_id)
        context = {'user': user}
        return render(self.request, self.template, context)
    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')

        print(card_name, card_number)
        models.CustomUser.objects.filter(id=user_id).update(card_name=card_name,card_number=card_number)
        return redirect(reverse_lazy('top_page'))


#ここから管理者側

#ユーザーリスト
class ManagementUserListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/user_list.html"
    model = models.CustomUser


class ManagementUserUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    template_name = 'management/user_list_update.html'
    form_class =forms.UserUpdateForm
    model = models.CustomUser
    success_url = reverse_lazy('user_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_user_id"] = self.request.path.split('/')[-2]
        
        return context
    

class ManagementUserDeleteView(onlyMnagementUserMixin, generic.DeleteView):
    model = models.CustomUser
    template_name = 'management/user_list_delete.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del_user_id = self.request.path.split('/')[-2]
        context["del_user"] = models.CustomUser.objects.get(id=del_user_id)

        return context

    


#カテゴリー
class ManagementCategoryListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/category_list.html"
    model = Category


class ManagementCategoryCreateView(onlyMnagementUserMixin, generic.CreateView):
    model = Category
    form_class = forms.CategoryCreateForm
    template_name = 'management/category_create.html'

class ManagementCategoryUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    model = Category
    form_class = forms.CategoryUpdateForm
    template_name = 'management/category_update.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_category_id"] = self.request.path.split('/')[-2]
        
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

        return context

#店舗
class ManagementRestaurantCreateView(onlyMnagementUserMixin, generic.CreateView):
    model = Restaurant
    template_name = 'management/restaurant_create.html'
    fields = '__all__'

class ManagementRestaurantListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/restaurant_manage_list.html"
    model = Restaurant

class ManagementRestaurantUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    template_name = 'management/restaurant_update.html'
    form_class = forms.RestaurantUpdateForm
    model = Restaurant
    success_url = reverse_lazy('restaurant_manage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["del_restaurant_id"] = self.request.path.split('/')[-2]
        
        return context

class ManagementRestaurantDeleteView(onlyMnagementUserMixin, generic.DeleteView):
    model = Restaurant
    template_name = 'management/restaurant_delete.html'
    success_url = reverse_lazy('restaurant_manage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del_restaurant_id = self.request.path.split('/')[-2]
        context["del_restaurant"] = Restaurant.objects.get(id=del_restaurant_id)

        return context


#売上
class ManagementSalesListView(onlyMnagementUserMixin, generic.ListView):
    template_name = 'management/sales.html'
    model = Sales






