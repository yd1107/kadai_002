from django.core.management.base import BaseCommand
import MeCab
import ipadic
from faker import Faker
from pykakasi import kakasi
from django.db import transaction
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from allauth.account.models import EmailAddress

dic_kana = {
  "知実" : "トモミ",
  "里佳" : "リカ",
  "七夏" : "ナナカ",
  "学" : "マナブ",
  "亮平" : "リョウヘイ",
  "裕太" : "ユウタ",
  "治" : "オサム",
  "聡太郎" : "ソウタロウ",
  "拓真" : "タクマ",
  "陽子" : "ヨウコ"

}


def KanaFromKanji(kanji):
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)
    kana = ''
    items = mecab.parse(kanji).split('\n')

    for item in items:
        words = item.split(',')
        if len(words) == 9:
            kana += words[7]

    return kana


class Command(BaseCommand):
    help = "ダミーユーザー生成"

    @transaction.atomic()
    def handle(self, *args, **options):
        fake = Faker('ja-JP')
        kks = kakasi()

        dic_username = {}
        i = 0

        while(True):
            name = fake.name()
            email = fake.email()
            zip_code = fake.zipcode() 
            address = fake.address()
            phone_number = fake.phone_number()
            job = fake.job()
            birth_day = fake.date_of_birth(minimum_age=18, maximum_age=70)

            last_name = name.split(' ')[0]        #侍
            last_kana = KanaFromKanji(last_name)  #サムライ

            first_name = name.split(' ')[1]       #太郎

            if first_name in dic_kana:
                first_kana = dic_kana[first_name]  #タロウ

            else:
                first_kana = KanaFromKanji(first_name)  #タロウ

            last_roman = kks.convert(last_kana)[0]["hepburn"]   #samurai
            first_roman = kks.convert(first_kana)[0]["hepburn"]  #taro

            user_name = last_roman + first_roman     #samuraitaaro
            email = first_roman + "." + last_roman + "@" + email.split("@")[1]

            if user_name in dic_username:
                continue

            dic_username[user_name] = email

            if i >= 5:
                break

            i = i + 1

            print(f"{last_name} {first_name} / {last_kana} {first_kana} / "
                  f"{email} / {address} / {zip_code} / {phone_number} / {job} /"
                  f"{birth_day}")
                    
            user = CustomUser()
            user.password = make_password("123456")
            user.username = user_name
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.user_name = name
            user.hurigana = f"{last_kana} {first_kana}"
            user.zip_code = zip_code
            user.address = address
            user.phone_number = phone_number
            user.birthday = birth_day.strftime("%Y%m%d")
            user.job = job

            user.save()

            email_adr = EmailAddress()
            email_adr.email = email
            email_adr.verified = 1
            email_adr.primary = 1
            email_adr.user_id = user.pk
            email_adr.save()

