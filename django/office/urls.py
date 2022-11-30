from django.urls import path
from . import views

app_name = "office"
urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro", views.pagina_cadastro, name="pagina-cadastro"),
    path("prelogin", views.pagina_login, name="pagina-login"),
    path("passageiro/procurar-carona", views.pagina_procurar_carona, name="pagina-procurar-carona"),
    path("motorista/criar-carona", views.organizar_motorista, name="organizar-motorista"),
    path("passageiro/busca-carona", views.pagina_escolher_grupo_carona, name="pagina-escolher-grupo-carona"),
    path("passageiro/precarona/<int:carona_id>", views.carona_pronto_passageiro, name="carona-pronto-passageiro"),
    path("motorista/precarona/<int:carona_id>", views.grupo_motorista, name="grupo-motorista"),
    path("passageiro/carona/<int:carona_id>", views.pagina_andamento_passageiro, name="pagina-andamento-passageiro"),
    path("motorista/carona/<int:carona_id>", views.pagina_andamento_motorista, name="pagina-andamento-motorista"),
    path("passageiro/poscarona/<int:carona_id>", views.carona_encerrada_passageiro, name="carona-encerrada-passageiro"),
    path("motorista/poscarona/<int:carona_id>", views.carona_encerrada_motorista, name="carona-encerrada-motorista"),

    path("api/carona/<int:carona_id>/juntarse", views.api_carona_juntarse, name="api-carona-juntarse"),
    path("api/carona/<int:carona_id>/iniciar", views.api_carona_iniciar, name="api-carona-iniciar"),
    path("api/carona/<int:carona_id>/encerrar", views.api_carona_encerrar, name="api-carona-encerrar"),
    path("api/carona/<int:carona_id>/avaliar", views.api_carona_avaliar, name="api-carona-avaliar"),
    path("api/carona/criar", views.api_carona_criar, name="api-carona-criar"),

    path("erro", views.erro_normal, name="erro"),
]
