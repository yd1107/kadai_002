from allauth.account.forms import SignupForm, LoginForm
from django import forms
from .models import CustomUser
from restaurant.models import Restaurant
from restaurant.models import Category
import datetime

CLOSE_DAYS_OF_WEEK = (
  (0, "日"),
  (1, "月"),
  (2, "火"),
  (3, "水"),
  (4, "木"),
  (5, "金"),
  (6, "土"),
)

PRICES = (
    (1000, "1,000円"),
    (1500, "1,500円"),
    (2000, "2,000円"),
    (2500, "2,500円"),
    (3000, "3,000円"),
    (3500, "3,500円"),
    (4000, "4,000円"),
    (4500, "4,500円"),
    (5000, "5,000円"),
    (5500, "5,500円"),
    (6000, "6,000円"),
    (6500, "6,500円"),
    (7000, "7,000円"),
    (7500, "7,500円"),
    (8000, "8,000円"),
    (8500, "8,500円"),
    (9000, "9,000円"),
)

TIMES = (
    (datetime.time(17, 0), '17:00'), (datetime.time(17, 30), '17:30'),
    (datetime.time(18, 0), '18:00'), (datetime.time(18, 30), '18:30'),
    (datetime.time(19, 0), '19:00'), (datetime.time(19, 30), '19:30'),
    (datetime.time(20, 0), '20:00'), (datetime.time(20, 30), '20:30'),
    (datetime.time(21, 0), '21:00'), (datetime.time(21, 30), '21:30'),
    (datetime.time(22, 0), '22:00'), (datetime.time(22, 30), '22:30'),
)

class MySignupForm(SignupForm):
    user_name = forms.CharField(max_length=255, label='氏名')
    hurigana = forms.CharField(max_length=255, label='フリガナ')
    zip_code = forms.CharField(max_length=255, label='郵便番号')
    address = forms.CharField(max_length=255, label='住所')
    phone_number = forms.CharField(max_length=255, label='電話番号')
    birthday = forms.CharField(max_length=255, label='誕生日')
    job = forms.CharField(max_length=255, label='職業')
    is_subscribed = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
      super(MySignupForm, self).__init__(*args, **kwargs)
      self.fields['user_name'].widget = forms.TextInput(attrs={'placeholder': '侍 太郎'})
      self.fields['hurigana'].widget = forms.TextInput(attrs={'placeholder': 'サムライ タロ'})
      self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '1010022'})
      self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '東京都千代田区神田棟堀町300番地'})
      self.fields['phone_number'].widget = forms.TextInput(attrs={'placeholder': '09012345678'})
      self.fields['birthday'].widget = forms.TextInput(attrs={'placeholder': '19950401'})
      self.fields['job'].widget = forms.TextInput(attrs={'placeholder': 'エンジニア'})
      self.fields['email'].widget = forms.TextInput(attrs={'type': 'email','placeholder':'taro.samurai@example.com'})
      self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
      self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
      
      def signup(self, request, user):
        user.user_name = self.cleaned_data['user_name']
        user.hurigana = self.cleaned_data['hurigana']
        user.zip_code = self.cleaned_data['zip_code']
        user.address = self.cleaned_data['address']
        user.phone_number = self.cleaned_data['phone_number']
        user.birthday = self.cleaned_data['birthday']
        user.job = self.cleaned_data['job']
        user.save()
        return user

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
      super(MyLoginForm, self).__init__(*args, **kwargs)
      self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'メールアドレス'})
      self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
      model = CustomUser
      fields = ('user_name', 'hurigana', 'zip_code', 'address', 'phone_number','birthday', 'job', )
    
    def __init__(self, *args, **kwargs):
          
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['user_name'].widget = forms.TextInput(attrs={'placeholder': '侍 太郎'})
      self.fields['hurigana'].widget = forms.TextInput(attrs={'placeholder': 'サムライ タロ'})
      self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '101-0022'})
      self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '東京都千代田区神田棟堀町300番地'})
      self.fields['phone_number'].widget = forms.TextInput(attrs={'placeholder': '090-1234-5678'})
      self.fields['birthday'].widget = forms.DateInput(attrs={"type":"date", "min":"1955-01-01", "max":"2007-12-31"})
      self.fields['job'].widget = forms.TextInput(attrs={'placeholder': 'エンジニア'})




class RestaurantInputForm(forms.ModelForm):
    name = forms.CharField(label='店舗名', max_length=64)
    description = forms.CharField(label='説明', max_length=128)
    price_min  = forms.IntegerField(label='価格帯')
    price_max  = forms.IntegerField(label='')
    zip_code = forms.CharField(label='郵便番号', max_length=32)
    address = forms.CharField(label='住所', max_length=128)
    open_time = forms.TimeField(label='営業時間')
    close_time = forms.TimeField(label='')
    close_day_of_week = forms.IntegerField(label='定休日')
    seats_number = forms.IntegerField(label='座席数')
    category = forms.ModelChoiceField(label="カテゴリ", queryset=Category.objects.all())
    photo = forms.ImageField(label='イメージ画像')

    class Meta:
      model = Restaurant
      fields = ('name', 'description', 'price_min', 'price_max', 
                'zip_code', 'address', 'open_time','close_time', 
                'close_day_of_week', 'seats_number', 'category', 'photo')

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['name'].widget = forms.TextInput(attrs={'placeholder': '店舗名', "class": "restaurant-name"})
      self.fields['description'].widget = forms.Textarea(attrs={'placeholder': '昔ながらの味をご堪能具ださい。'})
      self.fields['price_min'].widget = forms.Select(choices=PRICES, attrs={'class': "restaurant-combo combo-first"})
      self.fields['price_max'].widget = forms.Select(choices=PRICES, attrs={'class': "restaurant-combo combo-last"})
      self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '101-0022'})
      self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '東京都千代田区神田棟堀町300番地', "class": "restaurant-address"})
      self.fields['open_time'].widget = forms.Select(choices=TIMES, attrs={'class': "restaurant-combo combo-first"})
      self.fields['close_time'].widget = forms.Select(choices=TIMES, attrs={'class': "restaurant-combo combo-last"})
      self.fields['close_day_of_week'].widget = forms.Select(choices=CLOSE_DAYS_OF_WEEK)
      self.fields['seats_number'].widget = forms.NumberInput(attrs={'placeholder': '20', "class": "restaurant-seats"})
      self.fields['photo'].widget = forms.ClearableFileInput()
      
    def clean(self):
      min_val = self.cleaned_data.get("price_min")
      max_val = self.cleaned_data.get("price_max")
      
      open_time = self.cleaned_data.get("open_time")
      close_time = self.cleaned_data.get("close_time")
      
      if max_val <= min_val:
        raise forms.ValidationError("価格上限は下限値より大きな必要があります！")
      
      if close_time <= open_time:
        raise forms.ValidationError("閉店時間は開店時間より遅い必要があります！")
      
      
      return self.cleaned_data

#カテゴリー
class CategoryCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=64, label='カテゴリー名')

    class Meta:
      model = Category
      fields = ('name', )

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['name'].widget = forms.TextInput(attrs={'placeholder': '和食'})



class CategoryUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=64, label='カテゴリー名')

    class Meta:
      model = Category
      fields = ('name', )

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'カテゴリー名'})