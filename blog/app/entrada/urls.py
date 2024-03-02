from django.urls import path

# importaciones de vista del views.py
from .import views

urlpatterns = [

    path('entradas/', views.EntryViews.as_view(), name="entradas"),
    path('entradas/<slug>/', views.EntryCategoriasId.as_view(), name="entradas_id"),

]
