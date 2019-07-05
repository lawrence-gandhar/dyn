#author : Lawrence Gandhar
# date : 6th March 2019

# Django settings from settings.py
from django.conf import settings

# Import models
from app.models import *
from django.contrib.auth.models import User

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring
from datetime import *


from app.helpers import user_management


#***************************************************************************************
#   Edit Task Template
##***************************************************************************************
#
def edit_task_form_template(id):
    try:
        task = Task_Table.objects.get(pk = int(id))
    except:
        return ''

    userlist = user_management.userlist()
    
    part_list = []
    obs_list = []
    
    participants = Task_Participant.objects.filter(task = task.id).values_list('participant', flat = True)
    for p in participants:
        part_list.append(p)

    observers = Task_Observer.objects.filter(task = task.id).values_list('observer', flat = True)
    for o in observers:
        obs_list.append(o)


    html = ['<div class="row form-group" style="margin-bottom:2px;margin-top:5px;">']
    html.append('<input type="hidden" value="'+str(task.id)+'" name="id">')
    html.append('<label for="subject" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Title</label>')
    html.append('<div class="col-md-9">')
    html.append('<input  autocomplete="off" type="text" class="form-control input-sm" id="subject" name="subject" value="'+task.subject+'" required>')
    html.append('</div>')
    html.append('</div>')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:5px;">')
    html.append('<label for="details" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Details</label>')
    html.append('<div class="col-md-9">')
    html.append('<textarea class="form-control" name="details">'+task.details+'</textarea>')
    html.append('</div>')
    html.append('</div>')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:10px;">')
    html.append('<label for="responsible_person" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Responsible Person</label>')
    html.append('<div class="col-md-9">')
    
    # responsible person list
    html.append('<select name="responsible_person" class="form-control">')
    for user in userlist:
        html.append('<option value="'+str(user["id"])+'"')
        if int(task.responsible_person_id) == int(user["id"]):
            html.append(" selected ")
        html.append('>'+user["first_name"].title()+" "+user["last_name"].title()+" ("+user["username"]+')</option>')
    html.append('</select>')

    html.append('</div>')
    html.append('</div>')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:10px;">')
    html.append('<label for="deadline" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Deadline</label>')
    html.append('<div class=" col-md-9 input-group date" id="datetimepicker1" style="padding-right: 10px;padding-left: 10px;">')
    html.append('<input autocomplete="off" type="text" class="form-control" name="deadline" value="'+(task.deadline).strftime("%Y-%m-%d %H:%M:%S")+'"/>')
    html.append('<span class="input-group-addon">')
    html.append('<i class="pe-7s-timer" style="color:#ffffff"></i>')
    html.append('</span>')
    html.append('</div>')
    html.append('</div>')
    html.append('<hr style="margin-top: 5px; margin-bottom: 10px">')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:5px;">')
    html.append('<label for="high_priority" class="col-md-2 control-label" style="text-align:right; line-height:30px; font-size:80%">High Priority</label>')
    html.append('<div class="col-md-1">')

    high_priority = 'checked' if task.high_priority else ''
    email_notification = 'checked' if task.email_notification else ''
    remind = 'checked' if task.remind else ''
    repeat = 'checked' if task.repeat else ''

    html.append('<input '+high_priority+' type="checkbox" value="1" id="high_priority" name="high_priority" style="margin-top:10px;">')
    html.append('</div>')
    html.append('<label for="email_notification" class="col-md-2 control-label" style="text-align:right; line-height:30px; font-size:80%">Email Notify</label>')
    html.append('<div class="col-md-1">')
    html.append('<input '+email_notification+' type="checkbox" value="1" id="email_notification" name="email_notification" style="margin-top:10px;">')
    html.append('</div>')
    html.append('<label for="remind" class="col-md-2 control-label" style="text-align:right; line-height:30px; font-size:80%">Remind</label>')
    html.append('<div class="col-md-1">')
    html.append('<input '+remind+' type="checkbox" value="1" id="remind" name="remind" style="margin-top:10px;">')
    html.append('</div>')
    html.append('<label for="repeat" class="col-md-2 control-label" style="text-align:right; line-height:30px; font-size:80%">Repeat</label>')
    html.append('<div class="col-md-1">')
    html.append('<input '+repeat+' type="checkbox" value="1" id="repeat" name="repeat" style="margin-top:10px;">')
    html.append('</div>')
    html.append('</div>')
    html.append('<hr style="margin-top: 0px; margin-bottom: 10px">')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:5px;">')
    html.append('<label for="observers" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Observers</label>')
    html.append('<div class="col-md-9">')
    
    #observers
    html.append('<select name="observers" class="form-control" multiple="multiple">')  
    for user in userlist:
        html.append('<option value="'+str(user["id"])+'"')
        if user["id"] in obs_list:
            html.append(' selected = "selected"')
        html.append('>'+user["first_name"].title()+" "+user["last_name"].title()+" ("+user["username"]+')</option>')
    html.append('</select>')
    html.append('</div>')
    html.append('</div>')
    html.append('<div class="row form-group" style="margin-bottom:2px;margin-top:5px;">')
    html.append('<label for="participants" class="col-md-3 control-label" style="text-align:right; line-height:30px; font-size:80%">Participants</label>')
    html.append('<div class="col-md-9">')

    #participants
    html.append('<select name="participants" class="form-control" multiple="multiple">')  
    for user in userlist:
        html.append('<option value="'+str(user["id"])+'"')
        if user["id"] in part_list:
            html.append(' selected = "selected"')
        html.append('>'+user["first_name"].title()+" "+user["last_name"].title()+" ("+user["username"]+')</option>')
    html.append('</select>')

    html.append('</div>')
    html.append('</div>')

    return safestring.mark_safe(''.join(html))

