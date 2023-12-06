from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser),
    path('register/', views.registerUser),
    path('home/', views.base),
]
