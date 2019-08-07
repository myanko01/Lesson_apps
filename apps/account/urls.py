from django.urls import path

from . import views

""" <int:pk> これをつけるのは、対象が一つの時。updateなら誰のidをアップデートするか。とか
    account_list.htmlの編集urlのaccount.idがこの:pkに入る。
"""

app_name = "account"

urlpatterns = [
    path('', views.AccountListView.as_view(), name='index'),  # polls/の下に何もない時は、view.pyのindex関数を呼び出すという意味
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.AccountUpdateView.as_view(), name='update'),
]


