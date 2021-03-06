from app.views import *
from django.contrib.auth.decorators import login_required


try:
    from django.urls import path, include, re_path
    urlpatterns = [
        path('', home, name='home'),
        path('forgot-password/', forgot_password, name='forgot_password'),
        path('user/register/', RegisterUserView.as_view(), name='register_user'),
        path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
        path('tasks/', login_required(TasksView.as_view()), name='tasks'),
        path('tasks/add_task/', add_task, name='add_task'),
        path('tasks/remove-observers/', remove_observers, name='remove_observers'),
        path('tasks/remove-participants/', remove_participants, name='remove_participants'),
        path('tasks/logs/', task_logs, name='task_logs'),
        path('tasks/edit_task_form/', edit_task_form, name='edit_task_form'),
        path('tasks/edit_task/', edit_task, name='edit_task'),
        re_path('tasks/(?P<id>[\d]+)/more-options/', login_required(MoreOptionsView.as_view()), name='more_options'),
    ]

except ImportError:
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', home, name='home'),
        url(r'forgot-password/$', forgot_password, name='forgot_password'),
        url(r'user/register/$', RegisterUserView.as_view(), name='register_user'),
        url(r'dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
        url(r'tasks/$', login_required(TasksView.as_view()), name='tasks'),
        url(r'tasks/add_task/$', add_task, name='add_task'),
        url(r'tasks/remove-observers/$', remove_observers, name='remove_observers'),
        url(r'tasks/remove-participants/$', remove_participants, name='remove_participants'),
        url(r'tasks/logs/$', task_logs, name='task_logs'),
        url(r'tasks/edit_task_form/$', edit_task_form, name='edit_task_form'),
        url(r'tasks/edit_task/$', edit_task, name='edit_task'),
        url(r'tasks/(?P<id>[\d]+)/more-options/$', login_required(MoreOptionsView.as_view()), name='more_options'),
    ]