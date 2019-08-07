from datetime import date

from django.test import TestCase
from django.urls import reverse

from apps.lesson.tests.factory import GenreFactory, LessonFactory


class TestCreateAccountLessonLogList(TestCase):
    def test1(self):
        """ getで通常のアクセスが出来るか、尚且つ表示内容があっているか"""
        response = self.client.get(reverse("billing:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "billing/billing_list.html")

    def test2(self):
        """ 指定日付の時請求一覧が表示されるかのテスト"""
        attending_date = date(2019, 8, 1)
        english_lesson = GenreFactory(name="英語")
        LessonFactory(genre=english_lesson, attending_date=attending_date)
        GenreFactory(name="ファイナンス")
        GenreFactory(name="プログラミング")

        response = self.client.get(reverse("billing:index"), data={"billing_yyyymm": "2019/08"})

        self.assertContains(response, "太宰治")
        self.assertContains(response, "1レッスン")
