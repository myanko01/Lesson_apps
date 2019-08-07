from datetime import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils import timezone


def create_month_choices():
    choices = []
    for i in range(0, 1+3):  # 直近3ヶ月を絞込み条件に設定
        base_date = timezone.localdate() - relativedelta(months=i)
        choices.append((datetime.strftime(base_date, "%Y/%m"), datetime.strftime(base_date, "%Y/%m")))
    return choices


class SearchForm(forms.Form):
    """ ここでレポートのフォームを作っている
    """

    # forms.ChoiceFieldで 変数billing_yyyymmの中身を綺麗にしてる(月日等以外ものを除外。月日(choices=create_month_choices))
    # create_month_choices　だけが入っている(billing_yyyymmには)
    billing_yyyymm = forms.ChoiceField(choices=create_month_choices, label="請求月", required=False)

    def clean_billing_yyyymm(self):
        # ここのcleaned_dataで綺麗にしたbilling_yyyymmを取り出し
        billing_yyyymm = self.cleaned_data["billing_yyyymm"]
        if billing_yyyymm:
            # ここで形を変え　値を返す
            return parser.parse(billing_yyyymm).date()
