
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.loginview, name='loginview'),
    path('signup/',views.signupview, name='signupview'),
    path('logout/',views.logout_view, name='logoutview'),
    # path('editprofile/',views.edit_view,name='editview'),
]
