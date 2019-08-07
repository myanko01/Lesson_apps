from datetime import date

from django.test import TestCase

from apps.account.models import Account
from apps.billing.aggregator import Aggregator
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
        """ 必要データを作成し、集計情報をプロパティに持ったオブジェクトが格納されたリストが
            返ってくるか。(1人の顧客に対して)
        """
        LessonFactory(genre=self.genre_dict["英語"])

        target_date = date(2019, 8, 1)
        lesson_log_list = Lesson.objects.filter(attending_date__year=target_date.year,
                                                attending_date__month=target_date.month)

        aggregator = Aggregator()
        actual = aggregator.get_monthly_billings(Account.objects.all(), lesson_log_list, self.genre_dict)

        self.assertEqual(len(actual), 1)
        # クラス確認
        billing = actual[0]

        # プロパティ確認
        self.assertEqual(billing.account_id, 1)
        self.assertEqual(billing.account_name, "太宰治")
        self.assertEqual(billing.genre_name_set, {"英語"})
        self.assertEqual(billing.genre_names, "")
        self.assertEqual(billing.genre_num, 1)
        self.assertEqual(billing.attend_num, 1)
