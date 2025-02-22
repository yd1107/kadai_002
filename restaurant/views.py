from datetime import date
from operator import attrgetter

from django.db.models import Avg
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.
from . import models
from . import forms


class TopPageView(generic.TemplateView):
    """ トップ画面=================================="""
    template_name = "top_page.html"
    # model = models.Restaurant
    # queryset = models.Restaurant.objects.order_by('-rate')
    # context_object_name = 'restaurant_list'

    def get_context_data(self, **kwargs):
        if 'price_min_session' in self.request.session:
            self.request.session['price_min_session'] = 0

        if 'price_max_session' in self.request.session:
            self.request.session['price_max_session'] = 0

        if 'keyword_session' in self.request.session:
            self.request.session['keyword_session'] = ''

        if 'category_session' in self.request.session:
            self.request.session['category_session'] = ''

        if 'select_sort' in self.request.session:
            self.request.session['select_sort'] = 'created_at'

        # context = super(TopPageView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        #　カテゴリー一覧取得
        category_list = models.Category.objects.all()

        #新規掲載店取得
        new_restaurant_list = models.Restaurant.objects.all().order_by("-created_at")[:6]

        review_list = models.Review.objects.values("restaurant").annotate(rate_ave=Avg("rate")).order_by("-rate_ave")[:6]

        restaurant_list = []

        for review in review_list:
            val = models.Restaurant.objects.filter(pk=review['restaurant']).get()
            val.rate_ave = review['rate_ave']
            restaurant_list.append(val)

        context.update({
            'category_list': category_list,
            'new_restaurant_list': new_restaurant_list,
            'restaurant_list': restaurant_list,
        })

        return context




""" 会社概要=================================="""
class CompanyView(generic.TemplateView):
    template_name = "layout/company.html"

""" 利用規約=================================="""
class TermsView(generic.TemplateView):
    template_name = "layout/terms.html"


class RestaurantDetailView(generic.DetailView):
    """ レストラン詳細画面=================================="""
    template_name = "restaurant/restaurant_detail.html"
    model = models.Restaurant

    def get_context_data(self, **kwargs):
        user = self.request.user
        pk = self.kwargs['pk']
        
        context = super().get_context_data(**kwargs)
        
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        
        is_favorite = False

        if user.is_authenticated:
            is_favorite = models.Favorite.objects.filter(user=user).filter(
                restaurant=restaurant).exists()
        
        review_obj = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = review_obj['rate__avg'] if review_obj['rate__avg'] is not None else 0

        rate_count = models.Review.objects.filter(restaurant=restaurant).count()

        context.update({
            'is_favorite': is_favorite,
            'average_rate': average_rate,
            'rate_count': rate_count,
        })

        return context

    def post(self, request, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))

        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))

        pk = kwargs['pk']
        restaurant = models.Restaurant.objects.filter(id=pk).first()

        is_favorite = models.Favorite.objects.filter(user=user).filter(
            restaurant=restaurant).exists()

        if is_favorite:
            models.Favorite.objects.filter(user=user).filter(
                restaurant=restaurant).delete() 
            is_favorite = False

        else:
            favorite = models.Favorite()
            favorite.restaurant = restaurant
            favorite.user = user
            favorite.save()
            is_favorite = True

        self.object = restaurant
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)



class RestaurantSearchView(generic.TemplateView):
    """ レストラン一覧画面=================================="""
    template_name = "restaurant/restaurant_search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _session = self.request.session     # セッション情報取得

        # URLクエリパラメータ取得
        search_type = self.request.GET.get("search_type")       # 検索種類


        if search_type is not None:     # 検索条件指定の場合 セッション情報クリア
            _session["keyword"] = ""
            _session["category"] = ""
            _session["price_min"] = -1
            _session["price_max"] = -1
            
            if search_type == "keyword":
                _session["keyword"] = self.request.GET.get("keyword")
            elif search_type == "category":
                _session["category"] = self.request.GET.get("category")
            elif search_type == "price":
                _session["price_min"] = int(self.request.GET.get("price_min"))
                _session["price_max"] = int(self.request.GET.get("price_max"))

            #　ソート条件初期化
            _session["date_salected"] = "selected"
            _session["price_selected"] = ""
            _session["rate_selected"] = ""
            select_sort = "created_at"
            sort_reverse = True
            
        else:                           # ソート要求の場合
            #　検索条件
            if _session["price_min"] != -1 or _session["price_max"] != -1:
                search_type = "price"
            elif _session["category"] != "":
                search_type = "category"
            else:
                search_type = "keyword"
        
            #　ソート条件
            _session["date_salected"] = ""
            _session["price_selected"] = ""
            _session["rate_selected"] = ""

            select_sort = self.request.GET.get("select_sort")

            if select_sort == "created_at":
                _session["date_selected"] = "selected"
                sort_reverse = True

            elif select_sort == "price_min":
                _session["price_selected"] = "selected"
                sort_reverse = False
            else:
                _session["rate_selected"] = "selected"
                sort_reverse = True
            

        # ソート情報でない場合 検索条件の内容を該当セッション変数に保存
        restaurant_list = []

        if search_type == "keyword":
            condition = Q(
                Q(name__icontains=_session["keyword"]) |
                Q(category__name__icontains=_session["keyword"]) |
                Q(address__icontains=_session["keyword"])
            )

        elif search_type == "category":
            condition = Q(category__name=_session["category"])

        elif search_type == "price":
            condition = Q(price_min__gte=_session["price_min"], price_max__lte=_session["price_max"])

        restaurant_list = models.Restaurant.objects.filter(condition)

        for restaurant in restaurant_list:
            review_obj = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
            restaurant.rate = review_obj['rate__avg'] if review_obj['rate__avg'] is not None else 0

            restaurant.review_num = models.Review.objects.filter(restaurant=restaurant).count()
        
        restaurant_list = list(restaurant_list)
        restaurant_list.sort(key=attrgetter(select_sort), reverse=sort_reverse)

        context = {
            "keyword": _session["keyword"],
            "category_selected": _session["category"],
            "price_min": _session["price_min"],
            "price_max": _session["price_max"],

            "date_selected": _session["date_selected"],
            "price_selected": _session["price_selected"],
            "rate_selected": _session["rate_selected"],
            
            "category_list": models.Category.objects.all(),
            "restaurant_list": restaurant_list,
        }

        return context


class FavoriteListView(generic.ListView):
    """ お気に入り一覧画面=================================="""
    model = models.Favorite
    template_name = 'favorite/favorite_list.html'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = models.Favorite.objects.filter(user_id=user_id).order_by('-created_at')
        return queryset

def favorite_delete(request):
    pk = request.GET.get('pk')
    is_success = True
    if pk:
        try:
            models.Favorite.objects.filter(id=pk).delete()
        except:
            is_success = False
        else:
            is_success = False
        
        return JsonResponse({'is_success': is_success})

class ReservationCreateView(generic.CreateView):
    """ 新規予約登録画面=================================="""
    template_name = "reservation/reservation_create.html"
    model = models.Reservation

    form_class = forms.ReservationCreateForm
    success_url = reverse_lazy('top_page')

    def get(self, request, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_subscribed:
            return super().get(request, **kwargs)

        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))

        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))
            
    def form_valid(self, form):
        user_instance = self.request.user
        restaurant_instance = models.Restaurant(id=self.kwargs['pk'])
        reservation = form.save(commit=False)
        reservation.user = user_instance
        reservation.restaurant = restaurant_instance
        reservation.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):

        pk = self.kwargs['pk']

        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2

        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        close_day_list = self.make_close_list(restaurant.close_day_of_week)

        context.update({
            'restaurant': restaurant,
            'close_day_list': close_day_list,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        return context

    def make_close_list(self, close_day):
        close_list = []
        if '月' in close_day:
            close_list.append(1)
        if '火' in close_day:
            close_list.append(2)
        if '水' in close_day:
            close_list.append(3)
        if '木' in close_day:
            close_list.append(4)
        if '金' in close_day:
            close_list.append(5)
        if '土' in close_day:
            close_list.append(6)
        if '日' in close_day:
            close_list.append(0)

        return close_list


class ReservationListView(generic.ListView):
    """ 予約一覧表示画面=================================="""
    model = models.Reservation
    template_name = 'reservation/reservation_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = models.Reservation.objects.filter(user_id=self.request.user.id).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ReservationListView, self).get_context_data(**kwargs)
        context.update({
            'today': date.today(),
        })
        return context

def reservation_delete(request):
    """ 予約の削除=================================="""
    pk = request.GET.get('pk')
    is_success = True
    if pk:
        try:
            models.Reservation.objects.filter(id=pk).delete()
        except:
            is_success = False
    else:
        is_success = False

    return JsonResponse({'is_success': is_success})

class ReviewListView(generic.ListView):
    """ レビューの一覧表示=================================="""
    template_name = "review/review_list.html"
    model = models.Review
    restaurant_id = None
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        restaurant_id = self.kwargs['pk']
        queryset = super(ReviewListView, self).get_queryset().order_by('-rate')
        return queryset.filter(restaurant=restaurant_id)
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewListView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        is_posted = models.Review.objects.filter(user=self.request.user).filter(restaurant=restaurant).exists()

        average_rate =models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        
        context.update({
            'restaurant': restaurant,
            'is_posted': is_posted,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
        })
        return context


class ReviewCreateView(generic.CreateView):
    template_name = "review/review_create.html"
    model = models.Review
    form_class = forms.ReviewCreateForm
    success_url = None

    def get(self, request, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_subscribed:
            return super().get(request, **kwargs)
        
        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))

        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))

    def form_valid(self, form):
        user_instance = self.request.user
        restaurant_instance = models.Restaurant(id=self.kwargs['pk'])
        review = form.save(commit=False)
        review.restaurant = restaurant_instance
        review.user = user_instance
        review.save()
        self.success_url = reverse_lazy('review_list', kwargs={'pk': self.kwargs['pk']})
        return super().form_valid(form)

    def form_invalid(self, form):
        self.success_url = reverse_lazy('review_create', kwargs={'pk': self.kwargs['pk']})
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()

        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        context.update({
            'restaurant': restaurant,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        return context


class ReviewUpdateView(generic.UpdateView):
    """ レビューの更新================================== """
    model = models.Review
    template_name = 'review/review_update.html'
    form_class = forms.ReviewCreateForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = models.Review.objects.filter(id=pk).first().restaurant.id
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        restaurant_id = models.Review.objects.filter(id=pk).first().restaurant.id
        restaurant = models.Restaurant.objects.filter(id=restaurant_id).first()
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2

        rate_count = models.Review.objects.filter(restaurant=restaurant).count()

        context.update({
            'restaurant': restaurant,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        return context

def review_delete(request):
    """ レビューの削除================================== """
    pk = request.GET.get('pk')
    is_success = True

    if pk:
        try:models.Review.objects.filter(id=pk).delete()
        
        except: is_success = False
    else:
        is_success = False

    return JsonResponse({'is_success': is_success})