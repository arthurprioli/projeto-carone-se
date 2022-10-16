from django.urls import path
from . import views

app_name = "office"
urlpatterns = [
    path("", views.index, name="index"),
    path("demo/passageiro.html", views.passageiro, name="passageiro"),
    path("demo/grupo-passageiro.html", views.grupo_passageiro, name="grupo-passageiro"),
    path("demo/grupo-motorista.html", views.grupo_motorista, name="grupo-motorista"),
    path("demo/organizar-motorista.html", views.organizar_motorista, name="organizar-motorista"),
    path("demo/carona-pronto-passageiro.html", views.carona_pronto_passageiro, name="carona-pronto-passageiro"),
    path("demo/carona-andamento-passageiro.html", views.carona_andamento_passageiro, name="carona-andamento-passageiro"),
    path("demo/carona-andamento-motorista.html", views.carona_andamento_motorista, name="carona-andamento-motorista")
    # path("user/<int:user_id>/", views.user, name="user"),
    # path("cadastro", views.cadastro, name="cadastro"),
    # path("cadastrar", views.cadastrar, name="cadastrar")
]
