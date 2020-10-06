from django.urls import path
from .views import (index, register, login_view, logout_view, profile, edit_profile)

app_name = 'accounts'
urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
