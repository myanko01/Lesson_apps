import random

import factory
from django.utils import timezone

from apps.account.tests.factory import AccountFactory
from apps.lesson.models import Genre, Lesson


class GenreFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'ジャンル{}'.format(n))
    basic_rate = 0

    class Meta:
        model = Genre


class LessonFactory(factory.django.DjangoModelFactory):
    account = factory.SubFactory(AccountFactory)
    genre = factory.SubFactory(GenreFactory)
    attending_hour = random.randint(1, 12)
    attending_date = timezone.localdate()

    class Meta:
        model = Lesson

