from django.contrib import admin
from .models import Blog
from django.contrib.auth.models import Group

# Register your models here.
admin.site.site_header ='Community Health Admin' #changes the header of the admin page
admin.site.register(Blog)
