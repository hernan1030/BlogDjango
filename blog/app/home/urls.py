from django.urls import path

# importaciones de vista del views.py
from .views import HomeViews

urlpatterns = [

    path('', HomeViews.as_view(), name="home"),

]
