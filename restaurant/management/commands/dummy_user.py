from django.core.management.base import BaseCommand
import MeCab
import ipadic
from faker import Faker
from pykakasi import kakasi


dic_kana = {
  "知実" : "トモミ",
  "里佳" : "リカ",
  "七夏" : "ナナカ",
  "学" : "マナブ",
  "亮平" : "リョウヘイ",
  "裕太" : "ユウタ",
  "治" : "オサム",
  "聡太郎" : "ソウタロウ",
  "拓真" : "タクマ"

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

    def handle(self, *args, **options):
        fake = Faker('ja-JP')
        kks = kakasi()

        for _ in range(5):
            name = fake.name()
            email = fake.email()
            zip_code = fake.zipcode() 
            address = fake.address()
            phone_number = fake.phone_number()
            job = fake.job()



            last_name = name.split(' ')[0]
            last_kana = KanaFromKanji(last_name)

            first_name = name.split(' ')[1]

            if first_name in dic_kana:
                first_kana = dic_kana[first_kana]

            else:
                first_kana = KanaFromKanji(first_name)

            last_roman = kks.convert(last_kana)[0]["hepburn"]
            first_roman = kks.convert(first_kana)[0]["hepburn"]

            email = first_roman + "." + last_roman + "@" + email.split("@")[1]



            print(f"{last_name} {first_name} / {last_kana} {first_kana} / "
                  f"{email} / " f"{address} / " f"{zip_code} / " f"{phone_number} / " f"{job} ") 
                    
