from django.contrib import admin

from .models import Carona, Usuario

class CaronaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Carona, CaronaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
