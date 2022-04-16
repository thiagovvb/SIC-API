from django.db import models
from django.contrib.auth.models import User
import datetime

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

    #Este método responde o pedido de informação e muda o status para "respondido"
    def answer_request(self,id,answer):
        request = super().get_queryset().get(pk = id)
        request.answer = answer
        request.status = 'respondida'
        request.save()
    
    #Método que abre um recurso sobre uma demanda e atualiza o status da demanda para "Recurso"
    def open_appeal(self,id,appeal):
        request = super().get_queryset().get(pk = id)
        request.status = 'recurso'
        appeal = InfoAppeal(original_request = request,
                            content = appeal)
        request.save()
        appeal.save()

    #Muda o status da demanda para finalizada caso o demandante esteja satisfeito com a resposta
    def finalize_request(self,id):
        request = super().get_queryset().get(pk = id)
        request.status = 'finalizada'
        request.save()

class InfoAppealManager(models.Manager):

    #Método que registra uma resposta para um recurso e registra a demanda como finalizada
    def answer_appeal(self,id,answer):

        #Atualiza a demanda
        request = InfoRequest.objects.get(pk = id)
        request.status = 'finalizada'

        #Registra a resposta
        appeal = super().get_queryset().get(original_request = request)
        appeal.answer = answer

        appeal.save()
        request.save()


        

# Modelo que implementa a demanda e os campos necessários
class InfoRequest(models.Model):

    demander = models.ForeignKey(User, on_delete= models.RESTRICT)
    content = models.TextField()
    answer = models.TextField(blank=True)
    open_date = models.DateTimeField(auto_now_add=True, blank=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default='aberta', choices=REQUEST_STATUS, max_length=40)
    objects = models.Manager()
    request_manager = InfoRequestManager()

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
    objects = models.Manager()
    request_manager = InfoAppealManager()
    
    # Retorna a data que o recurso vence
    @property
    def expiration_date(self):
        return self.open_date + datetime.timedelta(days=15)