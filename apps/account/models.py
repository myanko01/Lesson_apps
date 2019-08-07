from django.db import models
from django.utils import timezone

from .consts import CHOICE_GENDER


class Account(models.Model):

    name = models.CharField('名前', max_length=50)
    gender = models.IntegerField('性別', choices=CHOICE_GENDER)
    age = models.IntegerField('年齢', default=0)
    created_at = models.DateTimeField("作成日時", default=timezone.now)  # 今の時間を指定
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return "{}({}) {}".format(self.name, self.age, self.get_gender_display())
        # get_gender_display()数字を引っ張ってきている。
        # 別に、return self.name とかでもよいが分かりやすいように上の記述。
