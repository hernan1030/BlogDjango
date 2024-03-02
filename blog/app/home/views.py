# vistas  basadas en clases
from django.views.generic import TemplateView, CreateView

# medelo entry de la app entrada
from app.entrada.models import Entry

# modelo home
from .models import Home, Contact
from app.entrada.models import Entry

# formularios
from .forms import HomePageForm, ContacForms

# para la carga de url
from django.urls import reverse_lazy
# Mis vistas aqui

# vista del home


class HomeViews(TemplateView):
    """Enviando los Entry al home """
    template_name = 'home/home.html'

    """
    Vista que renderiza la página de inicio (home.html).

    - Envia el contexto con el modelo Entry, Home y Contact.
    - Trae el formulario y lo envia al home.html.

    Attributes:
        template_name (str): Nombre de la plantilla HTML que se renderizará.
    """

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        # contexto sobre nosotros
        contex['p_principal'] = Home.objects.latest('created')
        # portada del blog
        contex['portada'] = Entry.objects.home_portada()

        # entradas en home
        contex['entradas_home'] = Entry.objects.entradas_en_home()

        # traigo el formulario y lo envio al home.html
        contex['form'] = HomePageForm
        return contex

# tiene en action en si template html que hace que se cargue la url si crear una vista aparte


class SuscriotorHomeViews(CreateView):
    # recibo en contex['form'] de la vista de arriba y carlo la urls solo para envio de correo
    form_class = HomePageForm
    success_url = reverse_lazy('home')

    """
    Vista para la suscripción en la página de inicio.

    - Recibe el formulario desde la vista 'HomeViews'.
    - Redirige a la página de inicio ('home') después de la suscripción.

    Attributes:
        form_class (class): Clase del formulario utilizado para la suscripción.
        success_url (str): URL a la que se redirige después de la suscripción.
    """


class ContacViews(CreateView):
    """
    este contacView hace caso lo mismo solo que aqui en formulario lo creamo 
    con la intencion que cada campo lo tome de forma individual,
    buscar en includes/footer.html ahi esta en formulario

    """
    model = Contact
    form_class = ContacForms
    success_url = reverse_lazy('home')
