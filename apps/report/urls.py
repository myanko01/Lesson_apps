from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='index'),
]
