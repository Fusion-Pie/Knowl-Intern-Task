from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser),
    path('register/', views.registerUser),
    path('profile/', views.profile),
    path('home/', views.base),
    path('l/', views.l),
    path('uploadFile/', views.uploadFile),
    path('viewUploadedFile/', views.viewUploadedFiles),
    path('searchUser/', views.searchUser),
    path('logout/', views.logoutUser),
]
