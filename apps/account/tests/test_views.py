from django.test import TestCase
from django.urls import reverse

from apps.account.models import Account
from apps.account.tests.factory import AccountFactory


class TestAccountListView(TestCase):
    """AccountListView のテストクラス"""

    def test1(self):
        """ getで通常のアクセスができるか : アカウントがある場合 """
        AccountFactory()
        response = self.client.get(reverse("account:index"))
        self.assertEqual(200, response.status_code)  # 正常にページが表示できることの確認
        self.assertTemplateUsed(response, "account/account_list.html")
        self.assertContains(response, "太宰治")  # 実際に表示されているhtmlの中身確認

    def test2(self):
        """ アカウントがない場合 """
        response = self.client.get(reverse("account:index"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "account/account_list.html")
        self.assertContains(response, "アカウントがありません")
        self.assertQuerysetEqual(response.context["account_list"], [])  # クエリセットがresponseの値の特定のリストを返す事を表明。


class TestAccountCreateView(TestCase):
    """AccountCreateView のテストクラス"""
    def test1(self):
        """ getで通常のアクセスができるか"""
        response = self.client.get(reverse("account:create"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "account/account_create.html")

    def test2(self):
        """ Accountモデルを使いデータを1件追加し(post)、値が帰ってくるか"""
        response = self.client.post(reverse("account:create"), data={"name": "江戸川乱歩", "gender": 1, "age": 30})
        self.assertRedirects(response, reverse("account:index"))
        self.assertEqual(Account.objects.count(), 1)  # レコード数
        account = Account.objects.first()
        self.assertTrue(account)
        self.assertEqual(account.name, "江戸川乱歩")
        self.assertEqual(account.gender, 1)
        self.assertEqual(account.age, 30)

    def test3(self):
        """バリデーションが通らなかった場合"""
        response = self.client.post(reverse('account:create'), data={'name': '', 'gender': 1, 'age': 20})
        self.assertEqual(400, response.status_code)  # 作成中
        self.assertTemplateUsed(response, 'account/account_create.html')
        self.assertFalse(response.context['form'].is_valid())


class TestAccountUpdate(TestCase):
    """ AccountUpdateView のテストクラス"""
    def test1(self):
        """ getで通常のアクセスが出来るかどうか"""
        account = AccountFactory()
        response = self.client.get(reverse("account:update", args=(account.id,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "account/account_update.html")

    def test2(self):
        """ idに関連づくアカウントがなかった場合"""
        response = self.client.get(reverse("account:update", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test3(self):
        """ name,ageを変更し、変更に基づく値が返ってくるか"""
        account = AccountFactory()
        response = self.client.post(reverse('account:update', args=(account.id,)), data={'name': '江戸川乱歩', 'gender': 2, 'age': 50})
        self.assertRedirects(response, reverse("account:index"))
        account.refresh_from_db()  # 更新(再ロード)
        self.assertEqual(account.name, "江戸川乱歩")
        self.assertEqual(account.gender, 2)
        self.assertEqual(account.age, 50)

    def test4(self):
        """ バリデーションが通らなかった場合"""
        account = AccountFactory()
        response = self.client.post(reverse('account:update', args=(account.id,)), data={'name': '', 'gender': 1, 'age': 20})
        self.assertEqual(400, response.status_code)
        self.assertTemplateUsed(response, 'account/account_update.html')
        self.assertFalse(response.context['form'].is_valid())
