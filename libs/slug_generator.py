import re
from django.utils.text import slugify as django_slugify
from unidecode import unidecode

def slugify(value):

    return '-'.join(value.split())
