# vitas basas en clases
from typing import Any
from django.views.generic import (ListView, DetailView)

# paginacin
from django.core.paginator import Paginator, EmptyPage


# modelo
from .models import Entry, Category

# Create your views here.


class EntryViews(ListView):
    template_name = 'entradas/entry.html'
    context_object_name = "entry"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['categorias'] = Category.objects.all()
        return contex

    def get_queryset(self):

        palabra_clave = self.request.GET.get('kware', '')
        categorias = self.request.GET.get('categorias', '')
        resultado = Entry.objects.buscar_entradas(palabra_clave, categorias)

        return resultado


class EntryCategoriasId(DetailView):
    template_name = 'entradas/entry_categorias.html'
    model = Entry
    context_object_name = "categorias"
