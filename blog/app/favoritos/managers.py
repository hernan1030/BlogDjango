from django.db import models


class ProfileEntada(models.Manager):

    def entradas_users(self, usuario):
        """filtrar en el modelo entry en public que este en true y user actual para hacer usado en la vista"""
        resultado = self.filter(
            entry__public=True,
            user=usuario
        )

        return resultado
