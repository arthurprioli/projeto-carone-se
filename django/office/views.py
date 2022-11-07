import typing
from office.models import Carona, Usuario
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.db.models import Model

# Create your views here.
def index(request):
    context = {}
    return render(request, "office/index.html", context)

def passageiro(request):
    context = {}
    return render(request, "office/passageiro.html", context)

def grupo_passageiro(request, carona_id):
    context = { "carona_id": carona_id }
    return render(request, "office/grupo-passageiro.html", context)

def organizar_motorista(request):
    context = {}
    return render(request, "office/organizar-motorista.html", context)

def pagina_login(request: HttpRequest):
    tipo = request.GET.get("tipo", "passageiro")
    context = { "login_motorista": tipo == "motorista" }
    return render(request, "office/login.html", context)

def pagina_cadastro(request):
    tipo = request.GET.get("tipo", "passageiro")
    context = { "login_motorista": tipo == "motorista" }
    return render(request, "office/cadastro.html", context)

def pagina_escolher_grupo_carona(request: HttpRequest):
    partida = request.GET.get("partida", "")
    if partida == "":
        caronas_objs = Carona.objects.all()
    else:
        caronas_objs = Carona.objects.filter(inicio=partida)

    caronas = []
    for carona in caronas_objs:
        motorista = { "nome": carona.motorista.nome }
        todos_passageiros = carona.passageiros.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        caronas.append({ "id": carona.pk, "motorista": motorista, "passageiros": passageiros })

    context = { "partida": partida or "(Qualquer)", "bairro": "Gávea", "caronas": caronas }
    return render(request, "office/pagina-escolher-grupo-carona.html", context)

def pagina_procurar_carona(request):
    context = {}
    return render(request, "office/pagina-procurar-carona.html", context)

# ---- Views específicos para as caronas ----

def carona_pronto_passageiro(request: HttpRequest, carona_id):  # passageiro/precarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome }
        todos_passageiros = carona.passageiros.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/carona-pronto-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

def grupo_motorista(request: HttpRequest, carona_id):  # motorista/precarona  - TODO: Pág Erro
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.passageiros.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/grupo-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

def pagina_andamento_passageiro(request: HttpRequest, carona_id):  # passageiro/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.passageiros.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

def pagina_andamento_motorista(request: HttpRequest, carona_id):  # motorista/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.passageiros.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

# -------------------------------------------
