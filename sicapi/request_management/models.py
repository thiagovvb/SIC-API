from django.db import models
from django.contrib.auth.models import User
import datetime

REQUEST_STATUS = [
    ('aberta', 'Aberta'),
    ('finalizada', 'Finalizada'),
    ('recurso', 'Recurso'),
    ('respondida', 'Respondida')
]

# Modelo que implementa a demanda e os campos necessários
class InfoRequest(models.Model):

    demander = models.ForeignKey(User, on_delete= models.RESTRICT)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default='aberta', choices=REQUEST_STATUS, max_length=40)

    # Retorna a data que a demanda vence
    @property
    def expiration_date(self):
        return self.open_date + datetime.timedelta(days=30)


# Modelo que implementa o recurso de uma demanda, que pode ou não ser aberto, dependendo da satisfação do usuário com a resposta original
class InfoAppeal(models.Model):

    original_request = models.ForeignKey(InfoRequest, on_delete=models.CASCADE)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    
    # Retorna a data que o recurso vence
    @property
    def expiration_date(self):
        return self.open_date + datetime.timedelta(days=15)