
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',views.loginview, name='loginview'),
    path('signup/',views.signupview, name='signupview'),
    path('logout/',views.logout_view, name='logoutview'),
    path('profile/edit',views.edit_profile_view,name='editprofile'),
    path('profile', views.profile, name='profile'),
    path('profile/sort/<int:sortid>', views.profilesort, name="profilesort"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
