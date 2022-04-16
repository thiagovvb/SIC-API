from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import pytz

REQUEST_STATUS = [
    ('aberta', 'Aberta'),
    ('finalizada', 'Finalizada'),
    ('recurso', 'Recurso'),
    ('respondida', 'Respondida')
]

class InfoRequestManager(models.Manager):

    #Este método retorna apenas os pedidos em aberto
    def get_open_requests(self):
        return super().get_queryset().filter(status = 'aberta')

    #Método que abre uma nova demanda
    def open_request(self, demander, content):
        new_request = InfoRequest(demander = demander, content = content)
        new_request.save()


# Modelo que implementa o recurso de uma demanda, que pode ou não ser aberto, dependendo da satisfação do usuário com a resposta original
class InfoAppeal(models.Model):

    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    
    # Retorna a data que o recurso vence
    @property
    def expiration_date(self):
        return self.open_date + datetime.timedelta(days=15)

# Modelo que implementa a demanda e os campos necessários
class InfoRequest(models.Model):

    demander = models.ForeignKey(User, on_delete= models.RESTRICT)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default='aberta', choices=REQUEST_STATUS, max_length=40)
    appeal = models.OneToOneField(InfoAppeal, on_delete=models.SET_NULL, default=None , blank=True , null=True)
    objects = models.Manager()
    request_manager = InfoRequestManager()

    #Este método responde o pedido de informação e muda o status para "respondido"
    def answer_request(self,answer):
        self.answer = answer
        self.answer_date = timezone.now()
        self.status = 'respondida'
        self.save()

    #Muda o status da demanda para finalizada caso o demandante esteja satisfeito com a resposta
    def finalize_request(self):
        self.status = 'finalizada'
        self.save()

    #Método que abre um recurso sobre uma demanda e atualiza o status da demanda para "Recurso"
    def open_appeal(self,appeal):
        self.status = 'recurso'
        appeal = InfoAppeal(content = appeal)
        self.appeal = appeal

        appeal.save()
        self.save()
        return appeal
        

    #Método que registra uma resposta para um recurso e registra a demanda como finalizada
    def answer_appeal(self,answer):

        #Atualiza a demanda
        self.status = 'finalizada'

        #Registra a resposta
        self.appeal.answer = answer
        self.appeal.answer_date = timezone.now()

        self.appeal.save()
        self.save()
        

    # Retorna a data que a demanda vence
    @property
    def expiration_date(self):
        return self.open_date + datetime.timedelta(days=30)

