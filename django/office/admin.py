from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Carona, Usuario

class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)

class CaronaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Carona, CaronaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
