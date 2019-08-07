from django.test import TestCase
from apps.lesson.tests.factory import GenreFactory, LessonFactory


class TestPayment(TestCase):
    """ lessonモデルのpayment関数のテスト"""
    def test1(self):
        """ 英語 : 4時間受講した場合 """
        genre = GenreFactory(name="英語", basic_rate=5000)
        lesson_log = LessonFactory(genre=genre, attending_hour=4)
        actual = lesson_log.payment()
        self.assertEqual(actual, 19000)

    def test2_ptn1(self):
        """ ファイナンス : 10時間受講した場合"""
        genre = GenreFactory(name="ファイナンス", basic_rate=0)
        lesson_log = LessonFactory(genre=genre, attending_hour=10)
        actual = lesson_log.payment()
        self.assertEqual(actual, 33000)

    def test2_ptn2(self):
        """ ファイナンス : 25時間受講した場合"""
        genre = GenreFactory(name="ファイナンス", basic_rate=0)
        lesson_log = LessonFactory(genre=genre, attending_hour=25)
        actual = lesson_log.payment()
        self.assertEqual(actual, 80000)

    def test2_ptn3(self):
        """ ファイナンス : 55時間受講した場合"""
        genre = GenreFactory(name="ファイナンス", basic_rate=0)
        lesson_log = LessonFactory(genre=genre, attending_hour=55)
        actual = lesson_log.payment()
        self.assertEqual(actual, 153500)

    def test3_ptn1(self):
        """ プログラミング : 4時間受講した場合"""
        genre = GenreFactory(name="プログラミング", basic_rate=20000)
        lesson_log = LessonFactory(genre=genre, attending_hour=4)
        actual = lesson_log.payment()
        self.assertEqual(actual, 20000)

    def test3_ptn2(self):
        """ プログラミング : 10時間受講した場合"""
        genre = GenreFactory(name="プログラミング", basic_rate=20000)
        lesson_log = LessonFactory(genre=genre, attending_hour=10)
        actual = lesson_log.payment()
        self.assertEqual(actual, 37500)

    def test3_ptn3(self):
        """ プログラミング : 25時間受講した場合"""
        genre = GenreFactory(name="プログラミング", basic_rate=20000)
        lesson_log = LessonFactory(genre=genre, attending_hour=25)
        actual = lesson_log.payment()
        self.assertEqual(actual, 87500)
    #

    def test3_ptn4(self):
        """ プログラミング : 55時間受講した場合"""
        genre = GenreFactory(name="プログラミング", basic_rate=20000)
        lesson_log = LessonFactory(genre=genre, attending_hour=55)
        actual = lesson_log.payment()
        self.assertEqual(actual, 164500)
