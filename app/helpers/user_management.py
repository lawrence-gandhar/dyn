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


#***************************************************************************************
#   Userlist : Excluding users with Admin authorization
#***************************************************************************************
#

def userlist():
    userlist = User.objects.filter(is_staff = False, is_active = True).values()
    return userlist

#***************************************************************************************
#   Username Already Exists
#***************************************************************************************
#

def username_exists(value=""):
    if len(value.strip()) > 0:
        if User.objects.filter(username = value):
            return True
    return False

#***************************************************************************************
#   Email Already Exists
#***************************************************************************************
#
def email_exists(value=""):
    if len(value.strip()) > 0:
        if User.objects.filter(email = value):
            return True
    return False