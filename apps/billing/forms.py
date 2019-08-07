from datetime import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils import timezone


def create_month_choices():
    choices = []
    for i in range(0, 1+3):
        base_date = timezone.localdate() - relativedelta(months=i)
        choices.append((datetime.strftime(base_date, "%Y/%m"), datetime.strftime(base_date, "%Y/%m")))
    return choices


class SearchForm(forms.Form):
    """ ここで請求月のフォームを作っている
    """

    billing_yyyymm = forms.ChoiceField(choices=create_month_choices, label="請求月", required=False)

    def clean_billing_yyyymm(self):

        billing_yyyymm = self.cleaned_data["billing_yyyymm"]
        if billing_yyyymm:

            return parser.parse(billing_yyyymm).date()
