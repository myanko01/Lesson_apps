from datetime import date

from django.test import TestCase
from django.urls import reverse

from apps.lesson.tests.factory import GenreFactory, LessonFactory


class TestReportListView(TestCase):
    """ TestReportListView のクラスのテスト"""
    def test1(self):
        """ getで通常のアクセスが出来るかどうかのテスト"""
        response = self.client.get(reverse("report:index"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "report/report_list.html")

    def test2(self):
        """ 指定日付の時レポート一覧が表示されるかのテスト"""
        attending_date = date(2019, 8, 1)
        english_lesson = GenreFactory(name="英語")
        LessonFactory(genre=english_lesson, attending_date=attending_date)
        GenreFactory(name="ファイナンス")
        GenreFactory(name="プログラミング")

        response = self.client.get(reverse("report:index"), data={"billing_yyyymm": "2019/08"})

        self.assertContains(response, "英語")
        self.assertContains(response, "ファイナンス")
        self.assertContains(response, "プログラミング")

    def test3(self):
        """ 対象月の受講データがなくても一覧が表示されるかの確認"""
        GenreFactory(name="英語")
        GenreFactory(name="ファイナンス")
        GenreFactory(name="プログラミング")

        response = self.client.get(reverse("report:index"), data={"billing_yyyymm": "2019/08"})

        self.assertContains(response, "ジャンル")
        self.assertContains(response, "性別")
        self.assertContains(response, "レッスン数")
        self.assertContains(response, "受講者数")
        self.assertContains(response, "売り上げ")

        self.assertContains(response, "年齢層別")
        self.assertContains(response, "10代")
        self.assertContains(response, "20代")
        self.assertContains(response, "30代")
        self.assertContains(response, "40代")
        self.assertContains(response, "50代")
        self.assertContains(response, "60代")
        self.assertContains(response, "70代")
        self.assertContains(response, "80代")
