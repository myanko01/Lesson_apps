from django.test import TestCase
from apps.lesson.tests.factory import GenreFactory, LessonFactory
from datetime import date
from apps.report.aggregator import ReportAggregator
from apps.billing.api import create_target_queryset_dict
from apps.account.tests.factory import AccountFactory
from pprint import pprint
from apps.report.aggregator import ReportRow


class TestAnalyeGenreGenderTrend(TestCase):
    """　analye_genre_gender_trend 関数のテスト"""
    def setUp(self):
        self.genre_dict = {
            "英語": GenreFactory(name="英語", basic_rate=5000),
            "ファイナンス": GenreFactory(name="ファイナンス", basic_rate=20000),
            "プログラミング": GenreFactory(name="プログラミング", basic_rate=0),
        }

    def test1(self):
        """ ジャンルと性別別に、選択年月のレッスン数・受講者数・売り上げ金額を表示するか確認
        """
        target_date = date(2019, 8, 1)
        billing_year = target_date.year
        billing_month = target_date.month
        target_queryset_dict = create_target_queryset_dict(billing_year, billing_month)

        # 男性顧客で各科目の受講を登録
        LessonFactory(genre=self.genre_dict["英語"], attending_date=target_date)
        LessonFactory(genre=self.genre_dict["ファイナンス"], attending_date=target_date)
        LessonFactory(genre=self.genre_dict["プログラミング"], attending_date=target_date)

        # 女性顧客で各科目の受講を登録
        account = AccountFactory(name="与謝野晶子", gender=2)
        LessonFactory(genre=self.genre_dict["英語"], account=account, attending_date=target_date)
        LessonFactory(genre=self.genre_dict["ファイナンス"], account=account, attending_date=target_date)
        LessonFactory(genre=self.genre_dict["プログラミング"], account=account, attending_date=target_date)

        aggregator = ReportAggregator()
        actual = aggregator.analye_genre_gender_trend(target_queryset_dict, self.genre_dict)

        self.assertEqual(len(actual), 6)
        # クラス確認
        # プロパティ確認
        # 男・ファイナンス
        report = actual[0]
        self.assertEqual(report.genre_name, "ファイナンス")
        # 女・ファイナンス
        report = actual[1]
        self.assertEqual(report.genre_name, "ファイナンス")
        # 男・プログラミング
        report = actual[2]
        self.assertEqual(report.genre_name, "プログラミング")
        # 女・プログラミング
        report = actual[3]
        self.assertEqual(report.genre_name, "プログラミング")
        # 男・英語
        report = actual[4]
        self.assertEqual(report.genre_name, "英語")
        # 女・英語
        report = actual[5]
        self.assertEqual(report.genre_name, "英語")


class TestAnalyeAgeGroupGenderTrend(TestCase):
    """ analye_age_group_gender_trend 関数のテスト"""
    def setUp(self):
        self.genre_dict = {
            "英語": GenreFactory(name="英語", basic_rate=5000),
            "ファイナンス": GenreFactory(name="ファイナンス", basic_rate=20000),
            "プログラミング": GenreFactory(name="プログラミング", basic_rate=0),
        }

    @staticmethod
    def setUp2(genre_dict):

        for gender in 1, 2:
            account_list = []
            # 世代毎に顧客を生成(男女別)
            for age in range(10, 90, 10):
                account_list.append(AccountFactory(gender=gender, age=age))
            # そして全顧客それぞれで全ジャンルの受講を登録
            # for genre_index in range(1, 4):
            for genre in ["ファイナンス", "プログラミング", "英語"]:
                for account in account_list:
                    LessonFactory(genre=genre_dict[genre], account=account)

    def test1(self):
        """ ジャンルと年齢層(性別)別に選択年月のレッスン数・受講者数・売り上げ金額を
            表示できるかの確認
        """
        TestAnalyeAgeGroupGenderTrend.setUp2(self.genre_dict)

        target_date = date(2019, 8, 1)
        billing_year = target_date.year
        billing_month = target_date.month
        target_queryset_dict = create_target_queryset_dict(billing_year, billing_month)

        aggregator = ReportAggregator()
        actual = aggregator.analye_age_group_gender_trend(target_queryset_dict, self.genre_dict)

        # リストの長さがあっているか確認
        self.assertEqual(len(actual), 48)
        # クラス確認
        for i in range(0, len(actual)):
            self.assertIsInstance(actual[i], ReportRow)

        age_group_number = 8
        # プロパティ確認
        # ファイナンス・男性の各年代の情報を確認(10代)
        for i in range(age_group_number):
            report = actual[i]
            age = f"{i + 1}0代"  # 10~80代生成
            self.assertEqual(report.genre_name, "ファイナンス")
            self.assertEqual(report.age_group, age)
            self.assertEqual(report.gender, 1)

            # ファイナンス・男性の20代の情報を確認
            report = actual[1]
            age = "20代"
            self.assertEqual(report.genre_name, "ファイナンス")
            self.assertEqual(report.age_group, age)

            # ファイナンス・男性の30代の情報を確認
            report = actual[10]
            age = "30代"
            self.assertEqual(report.genre_name, "ファイナンス")
            self.assertEqual(report.age_group, age)

            # プログラミング・男性50代の情報を確認
            report = actual[20]
            age = "50代"
            self.assertEqual(report.genre_name, "プログラミング")
            self.assertEqual(report.age_group, age)

            # 英語・男性70代の情報を確認
            report = actual[38]
            age = "70代"
            self.assertEqual(report.genre_name, "英語")
            self.assertEqual(report.age_group, age)

            # 英語・女性80代の情報を確認
            report = actual[47]
            age = "80代"
            self.assertEqual(report.genre_name, "英語")
            self.assertEqual(report.age_group, age)
