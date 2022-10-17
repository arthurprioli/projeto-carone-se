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
    path("demo/pagina-andamento-passageiro.html", views.pagina_andamento_passageiro, name="pagina-andamento-passageiro"),
    path("demo/pagina-andamento-motorista.html", views.pagina_andamento_motorista, name="pagina-andamento-motorista"),
    path("demo/pagina-escolher-grupo-carona.html", views.pagina_escolher_grupo_carona, name="pagina-escolher-grupo-carona"),
    path("demo/pagina-procurar-carona.html", views.pagina_procurar_carona, name="pagina-procurar-carona"),
    path("demo/cadastro.html", views.pagina_cadastro, name="pagina-cadastro"),
    path("demo/login.html", views.pagina_login, name="pagina-login")
    # path("user/<int:user_id>/", views.user, name="user"),
    # path("cadastro", views.cadastro, name="cadastro"),
    # path("cadastrar", views.cadastrar, name="cadastrar")
]
