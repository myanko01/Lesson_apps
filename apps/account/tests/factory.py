import factory

from apps.account.models import Account


class AccountFactory(factory.django.DjangoModelFactory):
    name = "太宰治"
    # name = factory.Sequence(lambda n: 'test_account{}'.format(n))
    gender = 1
    age = 20

    class Meta:
        model = Account
