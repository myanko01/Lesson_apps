from django.utils import timezone
from django.views import generic

from apps.account.models import Account
from apps.lesson.models import Lesson
from .aggregator import Aggregator
from .api import get_genre_data
from .forms import SearchForm


class BillingListView(generic.ListView):
    model = Account
    template_name = "billing/billing_list.html"

    def create_account_lesson_log_list(self):
        form = SearchForm(self.request.GET)
        form.is_valid()

        billing_yyyymm = form.cleaned_data['billing_yyyymm']

        if not billing_yyyymm:
            billing_yyyymm = timezone.localdate()

        lesson_log_list = Lesson.objects.filter(attending_date__year=billing_yyyymm.year,
                                                attending_date__month=billing_yyyymm.month).select_related('account', 'genre')

        genre_dict = get_genre_data()
        aggregate = Aggregator()
        billing_result_list = aggregate.get_monthly_billings(Account.objects.all(), lesson_log_list, genre_dict)

        return billing_result_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET)

        context["aggregate_result"] = self.create_account_lesson_log_list()

        return context
