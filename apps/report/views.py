from django.utils import timezone
from django.views import generic

from apps.account.models import Account
from apps.billing.api import get_genre_data, create_target_queryset_dict
from apps.report.forms import SearchForm
from .aggregator import ReportAggregator


class ReportListView(generic.ListView):
    model = Account
    template_name = "report/report_list.html"

    def create_report_list(self):
        form = SearchForm(self.request.GET)
        form.is_valid()

        billing_yyyymm = form.cleaned_data['billing_yyyymm']

        if not billing_yyyymm:
            billing_yyyymm = timezone.localdate()
        billing_yyyy, billing_mm = billing_yyyymm.year, billing_yyyymm.month

        query_dict = create_target_queryset_dict(billing_yyyy, billing_mm)

        genre_dict = get_genre_data()

        genre_gender_aggregate = ReportAggregator()
        lesson_gender_analysis_result = genre_gender_aggregate.analye_genre_gender_trend(query_dict, genre_dict)

        genre_age_aggregate = ReportAggregator()
        lesson_age_analysis_result = genre_age_aggregate.analye_age_group_gender_trend(query_dict, genre_dict)

        return lesson_gender_analysis_result, lesson_age_analysis_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = SearchForm(self.request.GET)
        context["lesson_gender_analysis_result"], context["lesson_age_analysis_result"] = self.create_report_list()

        return context
