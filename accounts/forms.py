from allauth.account.forms import SignupForm, LoginForm
from django import forms
from .models import CustomUser
from restaurant.models import Restaurant
from restaurant.models import Category

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
      self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '1010022'})
      self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '東京都千代田区神田棟堀町300番地'})
      self.fields['phone_number'].widget = forms.TextInput(attrs={'placeholder': '09012345678'})
      self.fields['birthday'].widget = forms.TextInput(attrs={'placeholder': '19950401'})
      self.fields['job'].widget = forms.TextInput(attrs={'placeholder': 'エンジニア'})


class RestaurantUpdateForm(forms.ModelForm):

    name = forms.CharField(label='店舗名', max_length=64)
    description = forms.CharField(label='説明', max_length=128)
    price = forms.CharField(label='価格帯', max_length=32)
    zip_code = forms.CharField(label='郵便番号', max_length=32)
    address = forms.CharField(label='住所', max_length=128)
    business_time = forms.CharField(label='営業時間', max_length=64)
    close_day_of_week = forms.CharField(label='定休日', max_length=32)
    seats_number = forms.CharField(label='座席数', max_length=32)
    category = forms.CharField(label='カテゴリー', max_length=32)


    class Meta:
      model = Restaurant
      fields = ('name', 'description', 'price', 'zip_code', 'address', 'business_time', 'close_day_of_week', 'seats_number', 'category',)

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['name'].widget = forms.TextInput(attrs={'placeholder': '店舗名'})
      self.fields['description'].widget = forms.TextInput(attrs={'placeholder': '昔ながらの味をご堪能具ださい。'})
      self.fields['price'].widget = forms.TextInput(attrs={'placeholder': '2,000円〜3,000円'})
      self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '1010022'})
      self.fields['address'].widget = forms.TextInput(attrs={'placeholder': '東京都千代田区神田棟堀町300番地'})
      self.fields['business_time'].widget = forms.TextInput(attrs={'placeholder': '11:00〜23:00'})
      self.fields['close_day_of_week'].widget = forms.TextInput(attrs={'placeholder': '水'})
      self.fields['seats_number'].widget = forms.TextInput(attrs={'placeholder': '22席'})
      self.fields['category'].widget = forms.TextInput(attrs={'placeholder': '和食'})


class CategoryUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=64, label='カテゴリー名')

    class Meta:
      model = Category
      fields = ('name', )

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""
      self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'カテゴリー名'})