from django.urls import reverse_lazy
from django.views import generic

from apps.lesson.models import Lesson


class LessonListView(generic.ListView):
    model = Lesson
    template_name = "lesson/lesson_list.html"
    queryset = Lesson.objects.select_related("account", "genre")


class LessonCreateView(generic.CreateView):
    model = Lesson
    template_name = "lesson/lesson_create.html"
    fields = ("account", "genre", "attending_date", "attending_hour")
    success_url = reverse_lazy("lesson:index")

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res


class LessonUpdateView(generic.UpdateView):
    model = Lesson
    template_name = "lesson/lesson_update.html"
    fields = ("account", "genre", "attending_date", "attending_hour")
    success_url = reverse_lazy("lesson:index")

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res
