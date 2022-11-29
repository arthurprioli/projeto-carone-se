from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import CharField, DateField, DateTimeField, FloatField, IntegerField

# Create your models here.
    
class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # null apenas por compatibilidade (NÃO DEVE ACONTECER NA PRÁTICA)
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    endereco = models.CharField(max_length=200)
    carona = models.ForeignKey("Carona", null=True, blank=True, on_delete=models.SET_NULL)  # pode não ter uma carona no momento.
    pontuacao = models.FloatField(default=0.0)
    max_pontos = models.FloatField(default=100.0)
    min_pontos = models.FloatField(default=0.0)

    def __str__(self):
        return f"Nome: {self.nome}; Gênero: {self.genero}; Endereço: {self.endereco}; Pontos: {self.pontuacao}\n"

class Carona(models.Model):
    destino = models.CharField(max_length=200)
    inicio =   models.CharField(max_length=100)
    data_hora = models.DateTimeField("data/hora")
    motorista = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_motorista")
    vagas = models.IntegerField(default=0)
    preco = models.FloatField("preço", default=0.)
    pontuacao = models.FloatField(default=0.0)
    max_pontos = models.FloatField(default=100.0)
    min_pontos = models.FloatField(default=0.0)

    def __str__(self):
        return f"Destino: {self.destino}. Início {self.inicio}. Data e hora: {self.data_hora}. Motorista: {self.motorista}. Vagas: {self.vagas} Preço: {self.preco} Pontos: {self.pontuacao}\n"

class Pontuacao(models.Model):
    pontuacao = models.FloatField()

    def __str__(self):
        return f"Pontuacao: {self.pontuacao} \n"
