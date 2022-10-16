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

def pagina_andamento_passageiro(request):
    context = {}
    return render(request, "office/pagina-andamento-passageiro.html", context)

def pagina_andamento_motorista(request):
    context = {}
    return render(request, "office/pagina-andamento-motorista.html", context)

def pagina_escolher_grupo_carona(request):
    context = {}
    return render(request, "office/pagina-escolher-grupo-carona.html", context)

def pagina_procurar_carona(request):
    context = {}
    return render(request, "office/pagina-procurar-carona.html", context)