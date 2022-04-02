from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('opennote/',views.open, name='open'),
    path('book',views.book, name="book"),
    path('register/', views.registerPage,name='register'),
    path('login/', views.loginPage,name='login'),
    
]