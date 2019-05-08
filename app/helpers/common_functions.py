#author : Lawrence Gandhar
# date : 8th May 2019

# Django settings from settings.py
from django.conf import settings

# Import models
from app.models import *
from django.contrib.auth.models import User

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

#
import string, re


#***************************************************************************************
#   Check Username provided is valid
#***************************************************************************************
#

def valid_username(value=""):
    if len(value.strip()) > 0:
        if re.match('^[a-zA-Z0-9._@]+$', value):
            return True
    return False

#***************************************************************************************
#   Check String is Only Ascii
#***************************************************************************************
#

def only_ascii(value=""):
    if len(value.strip()) > 0:
        if value.isascii():
            return True
    return False

#***************************************************************************************
#   Return string removing non printable characters
#***************************************************************************************
#

def clean_data(value=""):
    if len(value.strip()) > 0:
        filtered_string = filter(lambda x: x in string.printable, value)
        return ''.join(filtered_string)
    return ''
