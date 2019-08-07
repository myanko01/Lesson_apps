from django.utils import timezone
from django.views import generic

from apps.account.models import Account
from apps.lesson.models import Lesson
from .api import get_genre_data
from .forms import SearchForm
from .aggregator import Aggregator


class BillingListView(generic.ListView):
    model = Account
    template_name = "billing/billing_list.html"

    def create_account_lesson_log_list(self):
        form = SearchForm(self.request.GET)
        form.is_valid()

        billing_yyyymm = form.cleaned_data['billing_yyyymm']

        if not billing_yyyymm:
            billing_yyyymm = timezone.localdate()

        # 年月データ取得
        # forms.pyで作ったbilling_yyyymmをfilterかけてyear,monthを作る(Lessonモデルの)
        # .select_related指定された外部キーのオブジェクトも一緒びに取ってくるというやつ
        # 年月、(account, genre)(Lessonモデル)という新しい一つの変数が出来た=lesson_log_list
        lesson_log_list = Lesson.objects.filter(attending_date__year=billing_yyyymm.year,
                                                attending_date__month=billing_yyyymm.month).select_related('account', 'genre')

        # 集計
        # ジャンルデータの取得
        genre_dict = get_genre_data()
        aggregate = Aggregator()
        billing_result_list = aggregate.get_monthly_billings(Account.objects.all(), lesson_log_list, genre_dict)

        # render("billing/billing_list.html", {"form": form, "aggregate_result": billing_result_list})
        # これについて、ListViewではrender使えない。(そもそもrequestも必要。)　ただ返してるだけになってる
        return billing_result_list

    # contextは辞書型のデータ
    def get_context_data(self, **kwargs):  # お決まり文句
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET)

        # ここで　billing_result_list　を持ってきている
        context["aggregate_result"] = self.create_account_lesson_log_list()

        return context
