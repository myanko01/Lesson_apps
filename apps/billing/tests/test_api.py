from django.test import TestCase
from apps.lesson.tests.factory import GenreFactory
from apps.billing.api import get_genre_data
from apps.lesson.models import Genre


class TestGetGenreData(TestCase):
    def test1(self):
        """ get_genre_data関数テスト
            key:ジャンルname, vale:lessonオブジェクト　というデータ構造の辞書が返ってくるのか
        """
        GenreFactory(name="英語", basic_rate=5000)
        GenreFactory(name="ファイナンス", basic_rate=0)
        GenreFactory(name="プログラミング", basic_rate=20000)

        actual = get_genre_data()
        self.assertEqual(actual, {
            "英語": Genre.objects.get(name="英語"),
            "ファイナンス": Genre.objects.get(name="ファイナンス"),
            "プログラミング": Genre.objects.get(name="プログラミング")
        })
