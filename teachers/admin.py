from django.contrib import admin

from .models import PastPaper, ZoomLink
from django.contrib.auth.models import User

admin.site.register(PastPaper)
admin.site.register(ZoomLink)
