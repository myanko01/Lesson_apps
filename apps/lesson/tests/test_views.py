import datetime

from django.test import TestCase
from django.urls import reverse

from apps.account.models import Account
from apps.account.tests.factory import AccountFactory
from apps.lesson.models import Genre, Lesson
from apps.lesson.tests.factory import LessonFactory, GenreFactory


class TestLessonListView(TestCase):
    """ LessonListView のテストクラス"""
    def test1(self):
        """ getで通常のアクセスが出来るか"""
        response = self.client.get(reverse("lesson:index"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_list.html")

    def test2(self):
        """ 受講履歴がない場合"""
        response = self.client.get(reverse("lesson:index"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_list.html")
        self.assertContains(response, "受講履歴がありません")
        self.assertQuerysetEqual(response.context["lesson_list"], [])


class TestLessonCreateView(TestCase):
    """ LessonCreateView のテストクラス"""
    def test1(self):
        """ getで通常のアクセスが出来るか"""
        response = self.client.get(reverse("lesson:create"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_create.html")

    def test2(self):
        """ データを1件追加後、リダイレクト出来るかの確認
            そのデータに基づく値が返ってくるか
        """

        account = Account.objects.create(name="山田太郎", gender=1, age=20)
        genre = Genre.objects.create(name="英語", basic_rate=5000)
        response = self.client.post(reverse("lesson:create"), data={"account": account.id,  # accountのid
                                                                    "genre": genre.id,  # genreのid
                                                                    "attending_date": datetime.date(2019, 5, 1),
                                                                    "attending_hour": 10})  # レッスン受講一覧fields
        self.assertRedirects(response, reverse("lesson:index"))
        lesson_log = Lesson.objects.first()
        self.assertEqual(lesson_log.account.id, 1)
        self.assertEqual(lesson_log.genre.id, 1)
        self.assertEqual(lesson_log.attending_date, datetime.date(2019, 5, 1))
        self.assertEqual(lesson_log.attending_hour, 10)

    def test3(self):
        """ バリデーションが通らなかった場合"""
        account = Account.objects.create(name="山田太郎", gender=1, age=20)
        genre = Genre.objects.create(name="英語", basic_rate=5000)
        response = self.client.post(reverse("lesson:create"),
                                    data={"account": account.id,
                                          "genre": genre.id,
                                          "attending_date": datetime.date(2019, 5, 1),
                                          "attending_hour": ""})
        self.assertEqual(400, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_create.html")
        self.assertFalse(response.context['form'].is_valid())


class TestLessonUpdate(TestCase):
    """ TestAccountUpdate のテストテストクラス"""
    def test1(self):
        """ getで通常のアクセスが出来るかどうか"""
        lesson = LessonFactory()
        response = self.client.get(reverse("lesson:update", args=(lesson.id,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_update.html")

    def test2(self):
        """ データ更新後、リダイレクト出来るかの確認
            そのデータに基づく値が返ってくるか
        """
        account = AccountFactory()
        genre = GenreFactory(id=1)
        lesson_log = LessonFactory()
        response = self.client.post(reverse("lesson:update", args=(lesson_log.id,)),
                                    data={"account": account.id,
                                          "genre": genre.id,
                                          "attending_date": datetime.date(2019, 5, 1),
                                          "attending_hour": 4})

        self.assertRedirects(response, reverse("lesson:index"))
        lesson_log.refresh_from_db()
        self.assertEqual(lesson_log.account.id, 1)
        self.assertEqual(lesson_log.genre.id, 1)
        self.assertEqual(lesson_log.attending_date, datetime.date(2019, 5, 1))
        self.assertEqual(lesson_log.attending_hour, 4)

    def test3(self):
        """ バリデーションが通らなかった場合"""
        lesson_log = LessonFactory()
        genre = GenreFactory()
        response = self.client.post(reverse("lesson:update", args=(lesson_log.id,)),
                                    data={"account": "",
                                          "genre": genre.id,
                                          "attending_date": datetime.date(2019, 5, 1),
                                          "attending_hour": 4})
        self.assertEqual(400, response.status_code)
        self.assertTemplateUsed(response, "lesson/lesson_update.html")
        self.assertFalse(response.context['form'].is_valid())
