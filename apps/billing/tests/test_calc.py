from datetime import date

from django.test import TestCase

from apps.billing.calc import calculate_account_billing
from apps.lesson.models import Lesson
from apps.lesson.tests.factory import GenreFactory, LessonFactory


class TestCalculateAccountBilling(TestCase):
    def setUp(self):
        self.genre_dict = {
            "英語": GenreFactory(name="英語", basic_rate=5000),
            "ファイナンス": GenreFactory(name="ファイナンス", basic_rate=20000),
            "プログラミング": GenreFactory(name="プログラミング", basic_rate=0),
        }

    def test1(self):
        """ 英語: 受講者が英語のレッスンを受講した時の計算"""
        # 受講履歴を1つ登録
        target_date = date(2019, 8, 1)
        LessonFactory(genre=self.genre_dict["英語"], attending_hour=10, target_date=target_date)
        lesson_log_list = Lesson.objects.filter(attending_date__year=target_date.year,
                                                attending_date__month=target_date.month)
        account_id = 1
        actual = calculate_account_billing(account_id, lesson_log_list, self.genre_dict)
        self.assertEqual(actual, 40000)
