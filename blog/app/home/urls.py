from django.urls import path

# importaciones de vista del views.py
from .import views

urlpatterns = [

    path('', views.HomeViews.as_view(), name="home"),

    # no crea una vista aparte desde el html con el action se carga esta urle y lo redirige al home nuevamnete
    path('add-suscription', views.SuscriotorHomeViews.as_view(),
         name="add-suscription"),

    path('add-suscription-contac', views.ContacViews.as_view(),
         name="add-suscription-contac"),
]
