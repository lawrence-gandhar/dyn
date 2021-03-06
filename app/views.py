# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# IntegrityError Exception for checking duplicate entry, 
# connection import to establish connection to database 
from django.db import IntegrityError, connection 

# Used for serializing object data to json string
from django.core.serializers.json import DjangoJSONEncoder 
from django.core.serializers import serialize

# Django HTTP Request
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, JsonResponse

# Generic views as Class
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views import View

# system imports
import sys, os, csv, json, datetime, calendar, re

# Django utils
from django.utils import timezone, safestring
from django.utils.decorators import method_decorator

# Django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Django Messaging Framework
from django.contrib import messages

# Conditional operators and exception for models
from django.db.models import Q, Count, Sum, Prefetch
from django.core.exceptions import ObjectDoesNotExist

# Paginator class import
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Models Import
from app.models import *
from app.forms import *
from app.helpers import user_management, tasks_management, common_functions



#
#***************************************************************************************
# Home/Index
#***************************************************************************************
def home(request):
    template_name = 'app/index.html'
    return render(request, template_name, {})


#
#***************************************************************************************
# Forgot Password
#***************************************************************************************
def forgot_password(request):
    template_name = 'registration/forgot_password.html'
    return render(request, template_name, {})


#
#***************************************************************************************
# Register user
#***************************************************************************************
class RegisterUserView(View):
    template_name = 'registration/register_user.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):

        data = {}

        if user_management.email_exists(request.POST["email"]):
            messages.error(request, '{} is already registered'.format(request.POST["email"]))
            return render(request, self.template_name, data)


        if common_functions.valid_username(request.POST["username"]):
            if user_management.username_exists(request.POST["username"]):
                messages.error(request, 'Username already exists')
                data["username"] = request.POST["username"]
                data["email"] = request.POST["email"]
                data["first_name"] = request.POST["firstname"]
                data["last_name"] = request.POST["lastname"]

                return render(request, self.template_name, data)
            else:
                user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["psw"])
                user.first_name = request.POST["firstname"] 
                user.last_name = request.POST["lastname"] 
                user.save()

                auth_user = authenticate(username=request.POST["username"], password=request.POST["psw"])
                login(request, auth_user)
                return redirect('/dashboard/')

#
#**************************************************************************************
# Create your views here.
#**************************************************************************************

class DashboardView(ListView):
    template_name = 'app/dashboard.html'

    model = User
    paginate_by = 2
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["css_files"] = []
        context["js_files"] = []

        return context

#
#**************************************************************************************
#   MENU CLASS
#**************************************************************************************

class TasksView(ListView):
    template_name = 'app/tasks.html'

    model = Task_Table
    paginate_by = 30
    ordering = ["-deadline"]
    
    def get_queryset(self):
        qs = super().get_queryset() 
        obj = qs.filter(Q(responsible_person = self.request.user) | Q(created_by = self.request.user)).select_related()
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["css_files"] = []
        context["js_files"] = ["vendor/moment/moment.js", "vendor/datetime/datetime.js", "vendor/select2/dist/js/select2.js", "js_files/tasks.js"]
                
        return context

#
#**************************************************************************************
#   ADD TASK
#**************************************************************************************

@login_required
def add_task(request):
    if request.is_ajax():

        subject = request.POST.get("subject", "")
        details = request.POST.get("details", "")
        responsible_person = request.POST.get("responsible_person", "")
        deadline = request.POST.get("deadline", "")
        high_priority = request.POST.get("high_priority", False)
        email_notification = request.POST.get("email_notification", False)
        remind = request.POST.get("remind", False)
        repeat = request.POST.get("repeat", False)

        try:
            responsible_person = User.objects.get(pk = int(responsible_person))
        except:
            return JsonResponse({'ret':False,'message':'Error Occurred! Check data.'})

        try:
            task_table = Task_Table(
                subject = re.sub(r'[^\x00-\x7F]+','',subject),
                details = re.sub(r'[^\x00-\x7F]+','',details),
                responsible_person = responsible_person,
                deadline = deadline,
                high_priority = high_priority,
                email_notification = email_notification,
                remind = remind,
                repeat = repeat,
                created_by = request.user,
            )

            task_table.save()

            #
            #   ADD OBSERVERS AND PARTICIPANTS IF ANY ADDED
            #
            observers = request.POST.getlist('observers')
            participants = request.POST.getlist('participants')

            log = ['Task Added by '+str(request.user.username)]

            for id in observers:
                task_observers = Task_Observer(
                    task_id = task_table.id,
                    observer_id = int(id),
                    created_by = request.user,
                )

                task_observers.save()

            if len(observers) > 0:
                log.append('Observers added')

            for id in participants:
                task_participants = Task_Participant(
                    task_id = task_table.id,
                    participant_id = int(id),
                    created_by = request.user,
                )

                task_participants.save()

            if len(participants) > 0:
                log.append('Participants added')

            #
            #   ADD LOGS
            try:
                task_log = Task_Logs(
                    task_id = task_table.id,
                    logs = '. '.join(log)
                )

                task_log.save()
                return JsonResponse({'ret':True,'message':'Data Added Successfully'})
            except:
                return JsonResponse({'ret':False,'message':'Task Failed! Check Data and try again'})
        except:
            return JsonResponse({'ret':False,'message':'Task Failed! Check Data and try again'})
    return JsonResponse({'ret':False,'message':'Operation Denied!'})

#
#**************************************************************************************
#   REMOVE OBSERVERS
#**************************************************************************************

@login_required
def remove_observers(request):
    if request.is_ajax():

        try:
            tasks = Task_Table.objects.get(pk = int(request.POST["id"]))
        except:
            return HttpResponse(0)

        task_obs = Task_Observer.objects.filter(task = tasks).delete()

        task_log = Task_Logs(
                    task_id = tasks.id,
                    logs = 'Observers removed by '+request.user.username
                )

        task_log.save()

        return HttpResponse(1)


#
#**************************************************************************************
#   REMOVE PARTICIPANTS
#**************************************************************************************

@login_required
def remove_participants(request):
    if request.is_ajax():
        try:
            tasks = Task_Table.objects.get(pk = int(request.POST["id"]))
        except:
            return HttpResponse(0)

        task_par = Task_Participant.objects.filter(task = tasks).delete()

        task_log = Task_Logs(
                    task_id = tasks.id,
                    logs = 'Participants removed by '+request.user.username
                )

        task_log.save()

        return HttpResponse(1)

#
#**************************************************************************************
#   TASK LOGS
#**************************************************************************************
@login_required
def task_logs(request):
    if request.is_ajax():
        try:
            tasks = Task_Table.objects.get(pk = request.POST["id"])
        except:
            return HttpResponse('')

        logs = Task_Logs.objects.filter(task = tasks).values()

        html = []
        for log in logs:
            html.append('<p style="padding:1px 5px 1px 5px; margin:0px; font-size:80%; color:#ffffff;"><span style="color:rgb(248, 169, 0)">['+log["created_on"].strftime("%d %b %Y, %H:%M:%S")+']</span> '+log["logs"]+'</p>')

        return HttpResponse(safestring.mark_safe(''.join(html)))
    return HttpResponse('')

#
#**************************************************************************************
#   EDIT TASK 
#**************************************************************************************
@login_required
def edit_task_form(request):
    if request.is_ajax():
        return HttpResponse(tasks_management.edit_task_form_template(request.POST["id"]))
    return HttpResponse('')

@login_required
def edit_task(request):
    if request.is_ajax() and request.POST["id"]:

        responsible_person = request.POST.get("responsible_person", "")

        try:
            responsible_person = User.objects.get(pk = int(responsible_person))
        except:
            return JsonResponse({'ret':False,'message':'Error Occurred! Check data.'})

        try:
            task = Task_Table.objects.get(pk = request.POST["id"])

            task.subject = request.POST.get("subject", "")
            task.details = request.POST.get("details", "")
            task.responsible_person = responsible_person
            task.deadline = request.POST.get("deadline", "")
            task.high_priority = request.POST.get("high_priority", False)
            task.email_notification = request.POST.get("email_notification", False)
            task.remind = request.POST.get("remind", False)
            task.repeat = request.POST.get("repeat", False)

            task.save()

            #
            #   ADD OBSERVERS AND PARTICIPANTS IF ANY ADDED
            #
            observers = request.POST.getlist('observers')
            participants = request.POST.getlist('participants')

            log = ['Task Edit by '+str(request.user.username)]

            if len(observers) > 0:
                Task_Observer.objects.filter(task = task).delete()

                for id in observers:
                    task_observers = Task_Observer(
                    task_id = task.id,
                    observer_id = int(id),
                    created_by = request.user,
                )

                task_observers.save()
                log.append('Observers added')

            if len(participants) > 0:
                Task_Participant.objects.filter(task = task).delete()

                for id in participants:
                    task_participants = Task_Participant(
                    task_id = task.id,
                    participant_id = int(id),
                    created_by = request.user,
                )

                task_participants.save()
                log.append('Participants added')

            #
            #   ADD LOGS
            try:
                task_log = Task_Logs(
                    task_id = task.id,
                    logs = '. '.join(log)
                )

                task_log.save()
                return JsonResponse({'ret':True,'message':'Data Edited Successfully'})
            except:
                return JsonResponse({'ret':False,'message':'Logging Failed! Check Data and try again'})

        except:
            return JsonResponse({'ret':False,'message':'Error Occurred! Contact Administrator.'})
    return JsonResponse({'ret':False,'message':'Error Occurred! Contact Administrator.'})


#
#**************************************************************************************
#   EDIT TASK 
#**************************************************************************************
class MoreOptionsView(View):
    template_name = 'app/task_more_options.html'

    data = dict()
    data["css_files"] = []
    data["js_files"] = ["vendor/moment/moment.js", "vendor/datetime/datetime.js","vendor/select2/dist/js/select2.js","js_files/tasks.js"]

    def get(self, request, id):
        try:
            self.data["task"] = Task_Table.objects.get(pk = int(id))
        except:
            return HttpResponse(status=404)

        return render(request, self.template_name, self.data)

    def post(self, request, id):
        self.data["task"] = Task_Table.objects.get(pk = int(id))
        
        try:
            obj = Task_Notification_Settings.objects.filter(task = self.data["task"])
            
            obj.notify_observer = int(request.GET.getlist('notify_observer', False))
            obj.notify_observer_by = int(request.GET.getlist('notify_observer_by', False))
            obj.notify_participant = int(request.GET.getlist('notify_participant', False))
            obj.notify_participant_by = int(request.GET.getlist('notify_participant_by', False))
            obj.notify_24_hrs_ago = int(request.GET.getlist('notify_24_hrs_ago', False))
            obj.notify_once_everyday = int(request.GET.getlist('notify_once_everyday', False))
            obj.stop_after_deadline = int(request.GET.getlist('stop_after_deadline', False))
            obj.enable_observer_reply = int(request.GET.getlist('enable_observer_reply', False))
            obj.enable_participant_reply = int(request.GET.getlist('enable_participant_reply', False))
        
        except Task_Notification_Settings.DoesNotExists:

            obj = Task_Notification_Settings(
                notify_observer = int(request.GET.getlist('notify_observer', False)),
                notify_observer_by = int(request.GET.getlist('notify_observer_by', False)),
                notify_participant = int(request.GET.getlist('notify_participant', False)),
                notify_participant_by = int(request.GET.getlist('notify_participant_by', False)),
                notify_24_hrs_ago = int(request.GET.getlist('notify_24_hrs_ago', False)),
                notify_once_everyday = int(request.GET.getlist('notify_once_everyday', False)),
                stop_after_deadline = int(request.GET.getlist('stop_after_deadline', False)),
                enable_observer_reply = int(request.GET.getlist('enable_observer_reply', False)),
                enable_participant_reply = int(request.GET.getlist('enable_participant_reply', False)),
            )

        finally:
            obj.save()
        return HttpResponse('')