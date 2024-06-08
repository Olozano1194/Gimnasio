from django.contrib import admin
from .models import RegistrarUsuarioGym, RegistrarUsuario, RegistrarUsuarioGymDay

# Register your models here.

# admin.site.register(RegistrarUsuario)

@admin.register(RegistrarUsuario)
class RegisterUserAdmin2(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'user', 'email', 'roles', 'password')
    list_editable = ( 'name', 'lastname', 'user', 'email', 'roles', 'password')


@admin.register(RegistrarUsuarioGym)
class RegisterUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'phone', 'address', 'dateInitial', 'dateFinal')
    list_editable = ( 'name', 'lastname', 'phone', 'address', 'dateInitial', 'dateFinal')


@admin.register(RegistrarUsuarioGymDay)
class RegisterUserAdminDay(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'phone', 'dateInitial', 'price')
    list_editable = ( 'name', 'lastname', 'phone', 'dateInitial', 'price')