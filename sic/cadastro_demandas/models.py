from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Demanda(models.Model):

    STATUS = (
        ('aberta','Aberta'),
        ('respondida','Respondida'),
        ('aberta-recurso','Recurso'),
        ('finalizada','Finalizada')
    )

    tipo_demanda = models.CharField(max_length=255)
    conteudo_demanda = models.TextField()
    autor = models.ForeignKey(User, on_delete = models.CASCADE)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_ultima_movimentacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS, default='aberta')