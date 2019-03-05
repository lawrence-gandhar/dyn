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

#
#**************************************************************************************
# Create your views here.
#**************************************************************************************

class HomeView(ListView):
    template_name = 'app/index.html'

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
    ordering = ["-created_on"]
    
    def get_queryset(self):
        qs = super().get_queryset() 
        obj = qs.filter(Q(responsible_person = self.request.user) | Q(created_by = self.request.user)).select_related()
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["css_files"] = []
        context["js_files"] = ["vendor/moment/moment.js", "vendor/datetime/datetime.js", "vendor/select2/dist/js/select2.js", "scripts/tasks.js"]
                
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
                task_participants = Task_Partipant(
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

        task_par = Task_Partipant.objects.filter(task = tasks).delete()

        task_log = Task_Logs(
                    task_id = tasks.id,
                    logs = 'Observers removed by '+request.user.username
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
def edit_task(request):
    if request.is_ajax():
        return HttpResponse('')
    return HttpResponse('')