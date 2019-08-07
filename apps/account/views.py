from django.urls import reverse_lazy
from django.views import generic
from .models import Account


class AccountListView(generic.ListView):  # ListViewは、一覧ページに使ったりする。今回は顧客一覧。
    model = Account
    template_name = "account/account_list.html"
    context_object_name = "account_list"  # context_object_nameは ListView の裏側の変数。初期設定済みでここで上書きされる、どの変数も。


class AccountCreateView(generic.CreateView):
    model = Account
    template_name = "account/account_create.html"
    fields = ("name", "gender", "age")  # 何を作るか。名前・性別・年齢(必須)
    success_url = reverse_lazy("account:index")  # 成功したら指定のurlへgo

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res


class AccountUpdateView(generic.UpdateView):  # 編集
    model = Account
    template_name = "account/account_update.html"
    fields = ("name", "gender", "age")
    success_url = reverse_lazy("account:index")

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res
