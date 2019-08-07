from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.account.models import Account


class Genre(models.Model):
    """ 新規登録時に必要なモデル。
    """
    name = models.CharField('ジャンル名', max_length=50, unique=True)
    basic_rate = models.IntegerField('基本料金')
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.name


""" account,genreは第一引数に'名前'を入れると引数が複数あるとエラーがでてしまうため、後ろにverbose_name=''
    をつけて記述するとエラーがでなくなる。
"""


class Lesson(models.Model):
    """ 一覧表示用のモデル。
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='受講者')  # モデル同士の紐付け"ForeignKey"
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='ジャンル')
    attending_hour = models.IntegerField('受講時間', validators=[MinValueValidator(1), MaxValueValidator(12)])
    attending_date = models.DateField('受講日')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return str(self.genre.name)

    def payment(self):
        measured_rate = 0

        if self.genre.name == "英語":
            measured_rate = self.genre.basic_rate + self.attending_hour * 3500

        if self.genre.name == "ファイナンス":
            if 20 > self.attending_hour:
                measured_rate = 3300 * self.attending_hour + self.genre.basic_rate
            elif 50 > self.attending_hour >= 20:
                measured_rate = 3300 * 20 + 2800 * (self.attending_hour - 20)
            elif self.attending_hour >= 50:
                measured_rate = 3300 * 20 + 2500 * 30 + 2500 * (self.attending_hour - 50)

        if self.genre.name == "プログラミング":

            if self.attending_hour < 5:
                measured_rate = self.genre.basic_rate
            elif 20 > self.attending_hour >= 5:
                measured_rate = self.genre.basic_rate + 3500 * (self.attending_hour - 5)
            elif 35 > self.attending_hour >= 20:
                measured_rate = self.genre.basic_rate + 0 * 5 + 3500 * 15 + 3000 * (self.attending_hour - 20)
            elif 50 > self.attending_hour >= 35:
                measured_rate = self.genre.basic_rate + 0 * 5 + 3500 * 15 + 2800 * 15 + 2800 * (self.attending_hour - 35)
            elif self.attending_hour >= 50:
                measured_rate = self.genre.basic_rate + 0 * 5 + 3500 * 15 + 2800 * 15 + 2500 * 15 + 2500 * (self.attending_hour - 50)

        return measured_rate

