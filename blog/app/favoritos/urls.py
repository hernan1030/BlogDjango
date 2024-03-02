from django.urls import path

# importaciones de vista del views.py
from .import views

urlpatterns = [

    path('profiles', views.ProfileViews.as_view(), name='profiles'),

    # agregar favoritos pasandole la pk a los views.py
    path('add-profiles/<pk>/',
         views.AgregarFavoritos.as_view(), name='add-profiles'),

    # eliminar entrada favoritos
    path('delete-profiles/<pk>/',
         views.DeleteFavoritos.as_view(), name='delete-profiles'),

]
