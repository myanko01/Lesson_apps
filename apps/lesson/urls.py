from django.urls import path
from . import views

app_name = 'lesson'

urlpatterns = [
    path('', views.LessonListView.as_view(), name='index'),
    path('create', views.LessonCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.LessonUpdateView.as_view(), name='update'),
]

