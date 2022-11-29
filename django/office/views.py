import typing
from office.models import Carona, Usuario
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Model
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm

# Create your views here.
def index(request):  # / (index)
    context = {}
    return render(request, "office/index.html", context)

def passageiro(request):  # passageiro/procurar-carona-old
    context = {}
    return render(request, "office/passageiro.html", context)

def grupo_passageiro(request, carona_id):  # passageiro/busca-carona-old
    context = { "carona_id": carona_id }
    return render(request, "office/grupo-passageiro.html", context)

def organizar_motorista(request):  # motorista/criar-carona
    context = {}
    return render(request, "office/organizar-motorista.html", context)

def pagina_login(request: HttpRequest):  # login
    tipo = request.GET.get("tipo", "passageiro")
    context = { "login_motorista": tipo == "motorista" }
    return render(request, "office/login.html", context)

def pagina_cadastro(request):  # cadastro
    context = {}
    if request.method  == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse("office:pagina-login"))
    else:
        form = CadastroForm()
    return render(request, "office/cadastro.html", context={"form":form})

def pagina_escolher_grupo_carona(request: HttpRequest):  # passageiro/busca-carona
    partida = request.GET.get("partida", "")
    if partida == "":
        caronas_objs = Carona.objects.all()
    else:
        caronas_objs = Carona.objects.filter(inicio=partida)

    caronas = []
    for carona in caronas_objs:
        motorista = { "nome": carona.motorista.nome }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        caronas.append({ "id": carona.pk, "motorista": motorista, "passageiros": passageiros })

    context = { "partida": partida or "(Qualquer)", "bairro": "Gávea", "caronas": caronas }
    return render(request, "office/pagina-escolher-grupo-carona.html", context)

def pagina_procurar_carona(request):  # passageiro/procurar-carona
    context = {}
    return render(request, "office/pagina-procurar-carona.html", context)

# ---- Views específicos para as caronas ----

@login_required
def carona_pronto_passageiro(request: HttpRequest, carona_id):  # passageiro/precarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome }
        todos_passageiros = carona.usuario_set.all()
        if request.user.usuario not in todos_passageiros:
            return erro_generico(request, "Você não está nessa carona", status=403)

        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/carona-pronto-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

@login_required
def grupo_motorista(request: HttpRequest, carona_id):  # motorista/precarona  - TODO: Pág Erro
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/grupo-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

@login_required
def pagina_andamento_passageiro(request: HttpRequest, carona_id):  # passageiro/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

@login_required
def pagina_andamento_motorista(request: HttpRequest, carona_id):  # motorista/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

@login_required
def carona_encerrada_passageiro(request: HttpRequest, carona_id):  # passageiro/poscarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = {
            "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros,
            "destino": carona.destino, "valor": carona.preco
            }
        return render(request, "office/carona-encerrada-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

@login_required
def carona_encerrada_motorista(request: HttpRequest, carona_id):  # motorista/poscarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros ]
        destino = carona.destino
        context = {
            "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros,
            "destino": carona.destino, "valor": carona.preco
            }
        return render(request, "office/carona-encerrada-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return HttpResponseNotFound("Carona inválida")

# -------------------------------------------


# --------------- Erro ----------------------

def erro_generico(request: HttpRequest, mensagem_erro: str, status=400):
    context = { "mensagem_erro": mensagem_erro }
    return render(request, "office/pagina-erro.html", context, status=status)

def erro_normal(request: HttpRequest):
    return erro_generico(request, request.GET.get("mensagem", ""))

def erro_404(request: HttpRequest, exception):
    return erro_generico(request, "404: Não encontrado", status=404)

def erro_500(request: HttpRequest):
    return erro_generico(request, "500: Erro interno do servidor", status=500)

def erro_403(request: HttpRequest, exception):
    return erro_generico(request, "403: Permissão negada", status=403)

def erro_400(request: HttpRequest, exception):
    return erro_generico(request, "400: Pedido inválido", status=400)

# -------------------------------------------
