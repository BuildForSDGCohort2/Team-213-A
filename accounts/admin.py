from django.contrib import admin
from .models import UserProfile

admin.site.site_header = 'Community Health System Admin'

admin.site.register(UserProfile)
