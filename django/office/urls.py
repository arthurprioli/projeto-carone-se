from django.urls import path
from . import views

app_name = "office"
urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro", views.pagina_cadastro, name="pagina-cadastro"),
    path("login", views.pagina_login, name="pagina-login"),
    path("passageiro/procurar-carona-old", views.passageiro, name="passageiro"),
    path("passageiro/procurar-carona", views.pagina_procurar_carona, name="pagina-procurar-carona"),
    path("motorista/criar-carona", views.organizar_motorista, name="organizar-motorista"),
    path("passageiro/busca-carona-old", views.grupo_passageiro, name="grupo-passageiro"),
    path("pasasgeiro/busca-carona", views.pagina_escolher_grupo_carona, name="pagina-escolher-grupo-carona"),
    path("passageiro/precarona", views.carona_pronto_passageiro, name="carona-pronto-passageiro"),
    path("motorista/precarona", views.grupo_motorista, name="grupo-motorista"),
    path("passageiro/carona", views.pagina_andamento_passageiro, name="pagina-andamento-passageiro"),
    path("motorista/carona", views.pagina_andamento_motorista, name="pagina-andamento-motorista"),
    # posteriormente: <int:carona_id>
]
