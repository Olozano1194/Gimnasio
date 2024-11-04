from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegistrarUsuario(models.Model):

    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    user = models.CharField(max_length=30, unique=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    OPCIONES_ROL = [
        ('usuario', 'Usuario Normal'),
        ('admin', 'Administrador')
    ]

    roles = models.CharField(max_length=7, choices=OPCIONES_ROL, default='usuario')

    password = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'RegistrarUsuario'
        verbose_name_plural = 'RegistrarUsuarios'
        db_table = 'RegistrarUsuario'

class RegistrarUsuarioGym(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    dateInitial = models.DateField(max_length=50)
    dateFinal = models.DateField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'RegistrarUsuarioGym'
        verbose_name_plural = 'RegistrarUsuarioGyms'
        db_table = 'RegistrarUsuarioGym'
    
class RegistrarUsuarioGymDay(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateInitial = models.DateField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'RegistrarUsuarioGymDay'
        verbose_name_plural = 'RegistrarUsuarioGymDays'
        db_table = 'RegistrarUsuarioGymDay'
    

