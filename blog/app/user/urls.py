from django.urls import path

# importaciones de vista del views.py
from . import views

urlpatterns = [

    path('register-user', views.RegisterViews.as_view(), name='register'),
    path('login', views.LoginViews.as_view(), name='login'),
    path('logout', views.LogoutViews.as_view(), name='logout'),
    path('password-change', views.UpdatePasswordViews.as_view(),
         name='password-change'),
    path('register-user/<int:pk>/',
         views.ConfirmacionEmailViews.as_view(), name='confi_email'),

]
