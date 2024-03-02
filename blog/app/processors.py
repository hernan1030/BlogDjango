from app.home.models import Home

# Este processor lo que hace es enviar el corre y el telefono al footer


def home_info(request):

    home = Home.objects.latest('created')

    return {
        'phone': home.phone,
        'correo': home.contact_email,
    }
