# vistas  basadas en clases
from django.views.generic import TemplateView

# Mis vistas aqui


class HomeViews(TemplateView):
    template_name = 'home/home.html'
