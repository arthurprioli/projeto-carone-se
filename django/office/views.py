from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, "office/index.html", context)

def passageiro(request):
    context = {}
    return render(request, "office/passageiro.html", context)

def grupo_passageiro(request):
    context = {}
    return render(request, "office/grupo-passageiro.html", context)

def grupo_motorista(request):
    context = {}
    return render(request, "office/grupo-motorista.html", context)

def organizar_motorista(request):
    context = {}
    return render(request, "office/organizar-motorista.html", context)

def passageiro(request):
    context = {}
    return render(request, "office/passageiro.html", context)


def carona_pronto_passageiro(request):
    context = {}
    return render(request, "office/carona-pronto-passageiro.html", context)

def carona_andamento_passageiro(request):
    context = {}
    return render(request, "office/carona-andamento-passageiro.html", context)

def carona_andamento_motorista(request):
    context = {}
    return render(request, "office/carona-andamento-motorista.html", context)
