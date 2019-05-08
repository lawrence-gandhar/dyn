from django import forms
from app.models import *


#
#   
#
class Task_Table_Form(forms.ModelForm):

    class Meta:
        model = Task_Table
        fields = ('subject', 'details', 'responsible_person', 'deadline', 'high_priority','email_notification', 'remind', 'repeat')

