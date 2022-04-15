from django.db import models
from django.contrib.auth.models import User

REQUEST_STATUS = [
    ('aberta', 'Aberta'),
    ('finalizada', 'Finalizada'),
    ('recurso', 'Recurso'),
    ('respondida', 'Respondida')
]

class InfoRequest(models.Model):

    demander = models.ForeignKey(User, on_delete= models.RESTRICT)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(default='aberta', choices=REQUEST_STATUS, max_length=40)

class InfoAppeal(models.Model):

    original_request = models.ForeignKey(InfoRequest, on_delete=models.CASCADE)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
