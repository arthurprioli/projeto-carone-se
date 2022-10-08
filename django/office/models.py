from django.db import models
from django.forms import CharField, DateField, DateTimeField, FloatField, IntegerField

# Create your models here.


class Carona(models.Model):
    destino = models.CharField(max_length=80)
    inicio =   models.CharField(max_length=80)
    data_hora = models.DateTimeField()
    motorista = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    vagas = models.IntegerField()
    preco = models.FloatField()

    def __str__(self):
        return f"Destino: {self.destino}. Inicio {self.inicio}. Data e hora: {self.data_hora}. Motorista: {self.motorista}. Genero: {self.genero} Vagas: {self.vagas} Preco: {self.preco} \n"

    
class Usuario(models.Model):
    nome = models.CharField(max_length=80)
    genero = models.CharField(max_length=1)
    endereco = models.CharField(max_length=100)

    def __str__(self):
        return f"Nome: {self.nome} genero: {self.genero}. Endereco: {self.endereco} \n"
class Pontuacao(models.Model):
    pontuacao = models.FloatField()

    def __str__(self):
        return f"Pontuacao: {self.pontuacao} \n"