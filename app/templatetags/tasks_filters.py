from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from app.models import *
from django.contrib.auth.models import User

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

# Helper File Import
#from crm.helpers import *

# use Library
register = template.Library()


#*********************************************************************************
#   GET OBSERVERS HTML
#*********************************************************************************

@register.simple_tag 
def get_observers(id = None):
    html = []

    if id is not None:
        try:
            task = Task_Table.objects.get(pk = int(id))
        except:
            return safestring.mark_safe(''.join(html))

        observers = Task_Observer.objects.filter(task = task.id).select_related('observer')
        
        for rec in observers:
            html.append('<span class="user-item pull-left" id="rec-'+str(rec.task_id)+'-'+str(rec.observer_id)+'">'+rec.observer.username+'</span>')
        return safestring.mark_safe(''.join(html))
        
    return safestring.mark_safe(''.join(html))


#*********************************************************************************
#   GET OBSERVERS HTML
#*********************************************************************************

@register.simple_tag 
def get_participants(id = None):
    html = []

    if id is not None:
        try:
            task = Task_Table.objects.get(pk = int(id))
        except:
            return safestring.mark_safe(''.join(html))

        participants = Task_Participant.objects.filter(task = task.id).select_related('participant')
        
        for rec in participants:
            html.append('<span class="user-item pull-left" id="rec-'+str(rec.task_id)+'-'+str(rec.participant_id)+'">'+rec.participant.username+'</span>')
        return safestring.mark_safe(''.join(html))
        
    return safestring.mark_safe(''.join(html))


#*********************************************************************************
#   IF OBSERVERS ARE PRESENT
#*********************************************************************************

@register.filter   
def observers_present(value):

    if value is not None:
        try:
            task = Task_Table.objects.get(pk = int(value))
        except:
            return False

        observers = Task_Observer.objects.filter(task = task).count()

        if observers > 0:
            return True
        return False   
    return False


#*********************************************************************************
#   IF OBSERVERS ARE PRESENT
#*********************************************************************************

@register.filter   
def participants_present(value):

    if value is not None:
        try:
            task = Task_Table.objects.get(pk = int(value))
        except:
            return False

        participants = Task_Participant.objects.filter(task = task).count()

        if participants > 0:
            return True
        return False   
    return False

