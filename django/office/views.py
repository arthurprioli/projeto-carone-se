import typing
import datetime
from office.models import Carona, Usuario
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Model
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, CriarCaronaForm

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

@login_required
def organizar_motorista(request):  # motorista/criar-carona
    if request.user and request.user.usuario and request.user.usuario.carona:  # usuário já está em uma carona
        return redirect(reverse("office:carona-pronto-passageiro", args=[request.user.usuario.carona.pk]))

    form = CriarCaronaForm()
    rendered_form = form.as_div()
    # context = { "form": rendered_form }
    context = { "form": form }
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
    if request.user.is_authenticated and request.user.usuario and request.user.usuario.carona:  # usuário já está em uma carona
        return redirect(reverse("office:carona-pronto-passageiro", args=[request.user.usuario.carona.pk]))

    partida = request.GET.get("partida", "")
    if partida == "":
        caronas_objs = Carona.objects.all()
    else:
        caronas_objs = Carona.objects.filter(inicio=partida)

    caronas = []
    for carona in caronas_objs:
        if carona.chegada is None:  # caronas não encerradas
            motorista = { "nome": carona.motorista.nome }
            todos_passageiros = carona.usuario_set.all()
            passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros if passageiro != carona.motorista ]
            caronas.append({ "id": carona.pk, "motorista": motorista, "passageiros": passageiros, "valor": carona.preco, "vagas": carona.vagas, "restantes": carona.vagas - len(passageiros), "partida": carona.partida })

    context = { "partida": partida or "(Qualquer)", "bairro": "Gávea", "caronas": caronas }
    return render(request, "office/pagina-escolher-grupo-carona.html", context)

def pagina_procurar_carona(request):  # passageiro/procurar-carona
    if request.user.is_authenticated and request.user.usuario and request.user.usuario.carona:  # usuário já está em uma carona
        return redirect(reverse("office:carona-pronto-passageiro", args=[request.user.usuario.carona.pk]))
    context = {}
    return render(request, "office/pagina-procurar-carona.html", context)

# ---- API ----

@login_required
def api_carona_juntarse(request: HttpRequest, carona_id):  # /api/carona/:id/juntarse
    if request.POST:
        usuario: Usuario = request.user.usuario
        if usuario.carona is not None:
            return redirect(reverse("office:carona-pronto-passageiro", args=[usuario.carona.pk]))
        else:
            try:
                carona: Carona = Carona.objects.get(pk=carona_id)
                if carona.partida or carona.chegada:
                    return erro_generico(request, "Esta carona já foi iniciada", status=403)
                elif len([psg for psg in carona.usuario_set.all() if psg != carona.motorista]) >= carona.vagas:
                    return erro_generico(request, "Esta carona já está cheia", status=403) 

                usuario.carona = carona
                usuario.save()
                return redirect(reverse("office:carona-pronto-passageiro", args=[carona.pk]))
            except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
                return erro_generico(request, "Carona inválida", status=404)
    else:
        return erro_400(request, None)

@login_required
def api_carona_iniciar(request: HttpRequest, carona_id):  # /api/carona/:id/iniciar (iniciar a carona)
    if request.POST:
        try:
            usuario: Usuario = request.user.usuario
            carona: Carona = Carona.objects.get(pk=carona_id)
            if carona.motorista != usuario:
                return erro_generico(request, "Você não é o motorista desta carona", status=403)
            elif carona.partida is not None:
                return erro_generico(request, "Esta carona já foi iniciada", status=400)
            elif carona.chegada is not None:
                return erro_generico(request, "Esta carona já foi encerrada", status=400)
            else:
                carona.partida = datetime.datetime.now()
                carona.save()
                return redirect(reverse("office:pagina-andamento-motorista", args=[carona.pk]))
        except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
            return erro_generico(request, "Carona inválida", status=404)
    else:
        return erro_400(request, None)

@login_required
def api_carona_encerrar(request: HttpRequest, carona_id):  # /api/carona/:id/encerrar (encerrar a carona)
    if request.POST:
        try:
            usuario: Usuario = request.user.usuario
            carona: Carona = Carona.objects.get(pk=carona_id)
            if carona.motorista != usuario:
                return erro_generico(request, "Você não é o motorista desta carona", status=403)
            elif carona.chegada is not None:
                return erro_generico(request, "Esta carona já foi encerrada", status=400)
            else:
                carona.chegada = datetime.datetime.now()
                if carona.partida is None:
                    carona.partida = carona.chegada

                carona.save()
                return redirect(reverse("office:carona-encerrada-motorista", args=[carona.pk]))
        except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
            return erro_generico(request, "Carona inválida", status=404)
    else:
        return erro_400(request, None)

@login_required
def api_carona_avaliar(request: HttpRequest, carona_id):  # /api/carona/:id/avaliar
    if request.POST:
        try:
            usuario: Usuario = request.user.usuario
            carona: Carona = Carona.objects.get(pk=carona_id)
            if carona.chegada is None:
                return erro_generico(request, "Esta carona ainda não foi encerrada", status=400)
            elif usuario not in carona.usuario_set.all():
                return erro_generico(request, "Você não é motorista ativo ou passageiro desta carona", status=403)
            else:
                usuario.carona = None  # usuário não está mais nesta carona
                usuario.save()

                if len(carona.usuario_set.all()) < 1:
                    carona.delete()  # não terá mais passageiros/motorista

                return redirect(reverse("office:index"))
        except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
            return erro_generico(request, "Carona inválida", status=404)
    else:
        return erro_400(request, None)

@login_required
def api_carona_criar(request: HttpRequest):  # /api/carona/criar
    if request.POST:
        usuario: Usuario = request.user.usuario
        if usuario.carona is not None:
            return redirect(reverse("office:carona-pronto-passageiro", args=[usuario.carona.pk]))
        else:
            form = CriarCaronaForm(request.POST)
            if form.is_valid():
                inicio = form.cleaned_data["inicio"]
                data_hora = form.cleaned_data["data_hora"]
                destino = form.cleaned_data["destino"]
                valor = form.cleaned_data["valor"]
                vagas = form.cleaned_data["vagas"]

                carona = Carona(
                    inicio=inicio, data_hora=data_hora, motorista=usuario,
                    vagas=vagas, preco=valor
                )
                carona.save()
                usuario.carona = carona
                usuario.save()
                return redirect(reverse("office:grupo-motorista", args=[carona.pk]))
            else:
                return erro_generico(request, "Dados de formulário inválidos", status=400)
    else:
        return erro_400(request, None)

# -------------

# ---- Views específicos para as caronas ----

@login_required
def carona_pronto_passageiro(request: HttpRequest, carona_id):  # passageiro/precarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome }
        if request.user.usuario == carona.motorista:
            return redirect(reverse("office:grupo-motorista", args=[carona_id]))
        elif request.user.usuario.carona != carona:
            return erro_generico(request, "Você não está nessa carona", status=403)

        if carona.chegada:  # carona já acabou
            return redirect(reverse("office:carona-encerrada-passageiro", args=[carona_id]))
        if carona.partida:  # carona já começou
            return redirect(reverse("office:pagina-andamento-passageiro", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/carona-pronto-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

@login_required
def grupo_motorista(request: HttpRequest, carona_id):  # motorista/precarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome }
        if request.user.usuario != carona.motorista:
            if request.user.usuario.carona == carona:
                return redirect(reverse("office:carona-pronto-passageiro", args=[carona_id]))
            else:
                return erro_generico(request, "Você não é o motorista dessa carona", status=403)

        if carona.chegada:  # carona já acabou
            return redirect(reverse("office:carona-encerrada-motorista", args=[carona_id]))
        if carona.partida:  # carona já começou
            return redirect(reverse("office:pagina-andamento-motorista", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()

        passageiros = [ { "nome": passageiro.nome } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros }
        return render(request, "office/grupo-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

@login_required
def pagina_andamento_passageiro(request: HttpRequest, carona_id):  # passageiro/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        if request.user.usuario == carona.motorista:
            return redirect(reverse("office:pagina-andamento-motorista", args=[carona_id]))
        elif request.user.usuario.carona != carona:
            return erro_generico(request, "Você não está nessa carona", status=403)

        if carona.chegada:  # carona já acabou
            return redirect(reverse("office:carona-encerrada-passageiro", args=[carona_id]))
        if not carona.partida:  # carona ainda não partiu
            return redirect(reverse("office:carona-pronto-passageiro", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

@login_required
def pagina_andamento_motorista(request: HttpRequest, carona_id):  # motorista/carona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        if request.user.usuario != carona.motorista:
            if request.user.usuario.carona == carona:
                return redirect(reverse("office:pagina-andamento-passageiro", args=[carona_id]))
            else:
                return erro_generico(request, "Você não é o motorista dessa carona", status=403)

        if carona.chegada:  # carona já acabou
            return redirect(reverse("office:carona-encerrada-motorista", args=[carona_id]))
        if not carona.partida:  # carona ainda não partiu
            return redirect(reverse("office:grupo-motorista", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        destino = carona.destino
        context = { "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros, "destino": carona.destino }
        return render(request, "office/pagina-andamento-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

@login_required
def carona_encerrada_passageiro(request: HttpRequest, carona_id):  # passageiro/poscarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        if request.user.usuario == carona.motorista:
            return redirect(reverse("office:carona-encerrada-motorista", args=[carona_id]))
        elif request.user.usuario.carona != carona:
            return erro_generico(request, "Você não está nessa carona", status=403)

        if not carona.chegada:  # carona ainda não acabou
            return redirect(reverse("office:pagina-andamento-passageiro", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()

        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        destino = carona.destino
        context = {
            "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros,
            "destino": carona.destino, "valor": carona.preco, "chegada": carona.chegada
            }
        return render(request, "office/carona-encerrada-passageiro.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

@login_required
def carona_encerrada_motorista(request: HttpRequest, carona_id):  # motorista/poscarona
    try:
        carona: Carona = Carona.objects.get(pk=carona_id)
        motorista = { "nome": carona.motorista.nome, "endereco": carona.motorista.endereco }
        if request.user.usuario.carona != carona:
            return erro_generico(request, "Você não é o motorista dessa carona", status=403)
        elif request.user.usuario != carona.motorista:
            return redirect(reverse("office:carona-encerrada-passageiro", args=[carona_id]))

        if not carona.chegada:  # carona ainda não acabou
            return redirect(reverse("office:pagina-andamento-motorista", args=[carona_id]))

        todos_passageiros = carona.usuario_set.all()
        passageiros = [ { "nome": passageiro.nome, "endereco": passageiro.endereco } for passageiro in todos_passageiros if passageiro != carona.motorista ]
        destino = carona.destino
        context = {
            "carona_id": carona_id, "motorista": motorista, "passageiros": passageiros,
            "destino": carona.destino, "valor": carona.preco, "chegada": carona.chegada
            }
        return render(request, "office/carona-encerrada-motorista.html", context)
    except (Carona.DoesNotExist, Carona.MultipleObjectsReturned):
        return erro_generico(request, "Carona inválida", status=404)

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
