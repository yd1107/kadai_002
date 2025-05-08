from django.shortcuts import render , redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic , View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.db.models import Q
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
        user_id = request.GET.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)

        session_id = request.GET.get('session_id')

        if session_id != "":        # 新規登録
            if not session_id or not user_id:
                return HttpResponse("Invalid request", status=400)

            # ユーザーの subscription 項目を更新
            session = stripe.checkout.Session.retrieve(
                session_id,
                expand=['subscription']
            )

            customer_id = session.customer  # 顧客ID
            subscription_id = session.subscription.id  # サブスクリプションID

            # サブスクリプションからデフォルトの支払い方法を取得
            subscription = stripe.Subscription.retrieve(subscription_id, expand=['default_payment_method'])
            payment_method = subscription.default_payment_method

        else:                       # 編集
            customer_id = user.stripe_customer_id
            subscription_id = user.stripe_subscription_id

            customer = stripe.Customer.retrieve(
                customer_id,
                expand=["invoice_settings.default_payment_method"]
            )

            payment_method = customer.invoice_settings.default_payment_method

            if payment_method is None:
                payment_methods = stripe.PaymentMethod.list(customer=customer_id, type="card")
                payment_method = payment_methods.data[0]

        # カード情報の取得
        if payment_method and payment_method['card']:
            card = payment_method['card']
            last4 = card['last4']
            brand = card['brand']
            exp_month = card['exp_month']
            exp_year = card['exp_year']

            user.is_subscribed = True
            user.stripe_customer_id = customer_id
            user.stripe_subscription_id = subscription_id
        else:
            last4 = ""
            brand = ""
            exp_month = 0
            exp_year = 0

            user.is_subscribed = False
            user.stripe_customer_id = ""
            user.stripe_subscription_id = ""

        user.stripe_card_last4 = last4
        user.stripe_card_brand = brand
        user.stripe_card_exp_month = exp_month
        user.stripe_card_exp_year = exp_year

        user.save()

        return redirect(reverse_lazy('top_page'))


class SubscribeEditView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'subscribe/subscribe_edit.html'

    def post(self, request):
        user_id = request.user.id
        user = get_object_or_404(CustomUser, id=user_id)

        # セッション作成
        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=f"{settings.YOUR_DOMAIN}/accounts/subscribe-success/?session_id=&user_id={request.user.id}",
        )

        return redirect(session.url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.user.id
        user = get_object_or_404(CustomUser, id=user_id)

        context["user"] = user

        return context


class SubscribeCancelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'subscribe/subscribe_cancel.html'

    def post(self, request):
        user_id = request.user.id
        user = get_object_or_404(CustomUser, id=user_id)

        stripe.Subscription.delete(user.stripe_subscription_id)
        user.is_subscribed = False
        user.stripe_customer_id = ""
        user.stripe_subscription_id = ""
        user.stripe_card_last4 = ""
        user.stripe_card_brand = ""
        user.stripe_card_exp_month = 0
        user.stripe_card_exp_year = 0

        user.save()

        return redirect(reverse_lazy('top_page'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.user.id
        user = get_object_or_404(CustomUser, id=user_id)

        context["user"] = user 

        return context





#ここから管理者側

#ユーザーリスト
class ManagementUserListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/user_list.html"
    model = models.CustomUser
    paginate_by = 20
    user_name = None
    user_email = None

    def get_queryset(self):
        self.user_name = self.request.GET.get("user-name")
        if self.user_name is None:
            self.user_name = ""

        self.user_email = self.request.GET.get("user-email")
        if self.user_email is None:
            self.user_email = ""

        conditions = Q(user_name__contains=self.user_name,
                       email__contains=self.user_email)

        self.queryset = CustomUser.objects.filter(conditions)

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "user"
        context["search_name"] = self.user_name
        context["search_email"] = self.user_email

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
    category_name = None

    def get_queryset(self):
        self.category_name = self.request.GET.get("category-name")
        if self.category_name is None:
            self.category_name = ""

        conditions = Q(name__contains=self.category_name)

        self.queryset = Category.objects.filter(conditions)

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "category"
        context["search_name"] = self.category_name

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
    form_class = forms.RestaurantInputForm
    template_name = 'management/restaurant_create.html'
    success_url = reverse_lazy('restaurant_manage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "restaurant"
        
        return context

class ManagementRestaurantListView(onlyMnagementUserMixin, generic.ListView):
    template_name = "management/restaurant_manage_list.html"
    model = Restaurant
    paginate_by = 20
    restaurant_name = None
    restaurant_address = None

    def get_queryset(self):
        self.restaurant_name = self.request.GET.get("restaurant-name")
        if self.restaurant_name is None:
            self.restaurant_name = ""

        self.restaurant_address = self.request.GET.get("restaurant-address")
        if self.restaurant_address is None:
            self.restaurant_address = ""

        conditions = Q(name__contains=self.restaurant_name,
                       address__contains=self.restaurant_address)

        self.queryset = Restaurant.objects.filter(conditions)

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "restaurant"
        context["search_name"] = self.restaurant_name
        context["search_address"] = self.restaurant_address

        return context


class ManagementRestaurantUpdateView(onlyMnagementUserMixin, generic.UpdateView):
    template_name = 'management/restaurant_update.html'
    form_class = forms.RestaurantInputForm
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
    
    def get_queryset(self):
        qs = Sales.objects.all().order_by("-year", "-month")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected"] = "sales"
        
        return context



