
#   author : Lawrence Gandhar
#   project : DYN
#
#   start Date : 28th Feb
#   updated On : 
#
#   Models related to Task Management
#

from django.db import models
from django.contrib.auth.models import User

#
#   TASK MODEL
#

class Task_Table(models.Model):
    subject = models.TextField(null = False, blank = False,)
    details = models.TextField(null = True, blank = True,)
    responsible_person = models.ForeignKey(User, on_delete = models.SET_NULL, db_index = True, null = True, related_name = 'responsible_person')
    deadline = models.DateTimeField(null = True, blank = True, db_index = True,)
    high_priority = models.BooleanField(default = False, db_index = True,)
    email_notification = models.BooleanField(default = False, db_index = True,)
    remind = models.BooleanField(default = False, db_index = True,)
    repeat = models.BooleanField(default = False, db_index = True,)
    completed = models.BooleanField(default = False, db_index = True,)
    created_by = models.ForeignKey(User, db_index = True, on_delete = models.SET_NULL, null = True,)
    created_on = models.DateTimeField(auto_now = True, db_index = True,)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'task_tbl'
        verbose_name_plural = 'Task Table'

#
#   TASK OBSERVER MODEL
#

class Task_Observer(models.Model):
    task = models.ForeignKey(Task_Table, null = False, blank = False, db_index = True, on_delete = models.CASCADE,)
    observer = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, related_name = 'observer',)
    created_by = models.ForeignKey(User, db_index = True, on_delete = models.SET_NULL, null = True,)
    created_on = models.DateTimeField(auto_now = True, db_index = True,)

    class Meta:        
        db_table = 'task_observers_tbl'
        verbose_name_plural = 'Task Observers Table'

#
#   TASK PARTICIPANTS MODEL
#

class Task_Partipant(models.Model):
    task = models.ForeignKey(Task_Table, null = False, blank = False, db_index = True, on_delete = models.CASCADE,)
    participant = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, related_name = 'participant',)
    created_by = models.ForeignKey(User, db_index = True, on_delete = models.SET_NULL, null = True,)
    created_on = models.DateTimeField(auto_now = True, db_index = True,)

    class Meta:        
        db_table = 'task_participants_tbl'
        verbose_name_plural = 'Task Participants Table' 

#
#   TASK LOGS MODEL
#

class Task_Logs(models.Model):
    task = models.ForeignKey(Task_Table, null = False, blank = False, db_index = True, on_delete = models.CASCADE,)
    logs = models.TextField(null = True, blank = True, )
    created_on = models.DateTimeField(auto_now = True, db_index = True,)

    class Meta:
        db_table = 'task_logs_tbl'
        verbose_name_plural = 'Task Logs Table'

#
#   TASK NOTIFICATIONS MODEL
#

class Task_Notification(models.Model):
    task = models.ForeignKey(Task_Table, null = False, blank = False, db_index = True, on_delete = models.CASCADE,)
    notified_to = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL, related_name = 'notified_to',)
    via_email = models.BooleanField(default = False, db_index = True,)
    via_popup = models.BooleanField(default = False, db_index = True,)
    created_on = models.DateTimeField(auto_now = True, db_index = True,)

    class Meta:
        db_table = 'task_notification_tbl'
        verbose_name_plural = 'Task Notification Table'


