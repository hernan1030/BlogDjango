from django.db import models


class EntryManagers(models.Manager):

    def home_portada(self):

        return self.filter(
            public=True,
            portada=True
        ).order_by('-created').first()

    def entradas_en_home(self):

        return self.filter(
            public=True,
            in_home=True
        ).order_by('-created')[:4]

    def buscar_entradas(self, kword, categorias):

        if categorias:
            filtrar = self.filter(
                category__short_name=categorias,
                title__icontains=kword,
                public=True
            )
        else:
            filtrar = self.filter(
                title__icontains=kword,
                public=True
            ).order_by('-created')

        return filtrar
