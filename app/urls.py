from django.urls import path, re_path

from app.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('dashboard/', login_required(HomeView.as_view()), name='dashboard'),
    path('tasks/', login_required(TasksView.as_view()), name='tasks'),
    path('tasks/add_task/', add_task, name='add_task'),
    path('tasks/remove-observers/', remove_observers, name='remove_observers'),
    path('tasks/remove-participants/', remove_participants, name='remove_participants'),
    path('tasks/logs/', task_logs, name='task_logs'),
    path('tasks/edit/', edit_task, name='edit_task'),
]