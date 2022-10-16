from django.db import models
from django.forms import CharField, DateField, DateTimeField, FloatField, IntegerField

# Create your models here.

    
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return f"Nome: {self.nome}; Gênero: {self.genero}; Endereço: {self.endereco} \n"

class Carona(models.Model):
    destino = models.CharField(max_length=200)
    inicio =   models.CharField(max_length=100)
    data_hora = models.DateTimeField("data/hora")
    motorista = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1)
    vagas = models.IntegerField(default=0)
    preco = models.FloatField("preço", default=0.)

    def __str__(self):
        return f"Destino: {self.destino}. Início {self.inicio}. Data e hora: {self.data_hora}. Motorista: {self.motorista}. Gênero: {self.genero} Vagas: {self.vagas} Preço: {self.preco} \n"

class Pontuacao(models.Model):
    pontuacao = models.FloatField()

    def __str__(self):
        return f"Pontuacao: {self.pontuacao} \n"
