from django.views import generic
from apps.account.models import Account
from apps.report.forms import SearchForm
from django.utils import timezone
from apps.billing.api import get_genre_data, create_target_queryset_dict
from .aggregator import ReportAggregator


class ReportListView(generic.ListView):
    model = Account
    template_name = "report/report_list.html"

    def create_report_list(self):
        form = SearchForm(self.request.GET)
        form.is_valid()

        billing_yyyymm = form.cleaned_data['billing_yyyymm']
        # Lesson(受講履歴)クエリの抽出、科目・性別ごとにリストの分けた辞書の取得
        if not billing_yyyymm:
            billing_yyyymm = timezone.localdate()
        billing_yyyy, billing_mm = billing_yyyymm.year, billing_yyyymm.month

        query_dict = create_target_queryset_dict(billing_yyyy, billing_mm)
        # ジャンルデータの取得
        genre_dict = get_genre_data()

        # 「ジャンルと性別別」集計
        genre_gender_aggregate = ReportAggregator()
        lesson_gender_analysis_result = genre_gender_aggregate.analye_genre_gender_trend(query_dict, genre_dict)

        # 「ジャンルと年齢層別」集計
        genre_age_aggregate = ReportAggregator()
        lesson_age_analysis_result = genre_age_aggregate.analye_age_group_gender_trend(query_dict, genre_dict)

        return lesson_gender_analysis_result, lesson_age_analysis_result

    def get_context_data(self, **kwargs):  # お決まり文句
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm(self.request.GET)
        # return で２つ返しているので、ここも同じ
        context["lesson_gender_analysis_result"], context["lesson_age_analysis_result"] = self.create_report_list()

        return context
