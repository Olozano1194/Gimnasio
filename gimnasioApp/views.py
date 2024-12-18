from django.shortcuts import render, redirect, get_object_or_404
from . forms import UsuarioForm, UsuarioFormGym, UsuarioFormGymDay, RenovacionForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from .models import RegistrarUsuario, RegistrarUsuarioGym, RegistrarUsuarioGymDay, Renovacion
from django.contrib.auth.decorators import login_required

from datetime import datetime, date
from django.utils import timezone

import bcrypt  #esto nos sirve para encriptar la contraseña...ojo debemos instalarla pip install bcrypt 

# Create your views here.
#Esta parte es la vista de los usuarios que se loguean
def Login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    
    else:
        user = request.POST['user'] 
        password=request.POST['password']

        #autenticamos el usuario
        user = authenticate(request, username=user, password=password)

        if user is None:
            # Si el usuario no se encuentra o la contraseña no es válida
            return render(request, 'login/login.html', {'error': 'Username or password is incorrect'})
        #Si el usuario existe, toca verificar la contraseña
        try:
            user_profile = RegistrarUsuario.objects.get(user=user)
        except RegistrarUsuario.DoesNotExist:
            return render(request, 'login/login.html', {'error': 'Username or password is incorrect'})
        
        #Verificamos la contraseña manualmente
        if bcrypt.checkpw(password.encode('utf-8'), user_profile.password.encode('utf-8')):
            #Guardamos la información en la sesión si la contraseña es correcta
            request.session['user_name'] = f'{user_profile.name} {user_profile.lastname}'
            request.session['user_roles'] = f'{user_profile.roles}' #se guarda el rol
            login(request, user) #Usamos Django para iniciar sesión
            return redirect('welcome')        
        else:
            return render(request, 'login/login.html', {'error': 'Username or password is incorrect'})

# @login_required
# def registerBd(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST)

#         if form.is_valid():
#             password = form.cleaned_data['password']
#             hashed_password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#             usuario = form.save(commit=False)
#             usuario.password= hashed_password.decode('utf-8') #Guardamos la contra como un string
#             usuario.save()
#             return redirect('login')
#     else:
#         form = UsuarioForm()
#     return render(request, 'checkIn.html', {'form': form})

@login_required
def singoff(request):
    logout(request)
    return redirect('login')

#@login_required
def formcheckinUser(request):
    if request.method == 'GET':
        return render(request, 'login/checkInLogin.html')
    
    if request.method == 'POST':
        username = request.POST['user']
        email = request.POST['email']
        
        # Verificaciones previas más específicas
        if RegistrarUsuario.objects.filter(user=username).exists():
            return render(request, 'login/checkInLogin.html', {
                'error': f'El nombre de usuario "{username}" ya está en uso',
                'form_data': request.POST
            })
            
        if RegistrarUsuario.objects.filter(email=email).exists():
            return render(request, 'login/checkInLogin.html', {
                'error': f'El email "{email}" ya está registrado',
                'form_data': request.POST
            })

        if request.POST['password'] != request.POST['repeatpassword']:
            return render(request, 'login/checkInLogin.html', {
                'error': 'Las contraseñas no coinciden',
                'form_data': request.POST
            })

        try:
            # Crear el hash de la contraseña fuera de la transacción
            hashed_password = bcrypt.hashpw(
                request.POST['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            with transaction.atomic():
                # Primero intentar crear el usuario personalizado
                usuario_personalizado = RegistrarUsuario.objects.create(
                    name=request.POST['name'],
                    lastname=request.POST['lastname'],
                    user=username,
                    email=email,
                    roles=request.POST['roles'],
                    password=hashed_password
                )
                
                # Si el usuario personalizado se creó exitosamente, crear el usuario de Django
                django_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=request.POST['password'],
                    first_name=request.POST['name'],
                    last_name=request.POST['lastname']
                )
                
                # Iniciar sesión
                #login(request, django_user)
                return redirect('login')

        except IntegrityError as e:
            # Para debugging
            print(f"Error de integridad: {str(e)}")
            error_message = 'El usuario o email ya existe'
            if 'user' in str(e):
                error_message = 'El nombre de usuario ya está en uso'
            elif 'email' in str(e):
                error_message = 'El email ya está registrado'
            
            return render(request, 'login/checkInLogin.html', {
                'error': error_message,
                'form_data': request.POST
            })
        except Exception as e:
            # Para debugging
            print(f"Error inesperado: {str(e)}")
            return render(request, 'login/checkInLogin.html', {
                'error': f'Error al crear el usuario: {str(e)}',
                'form_data': request.POST
            })

    return render(request, 'checkInLogin.html')

#@login_required
def welcome(request):
    UserGymList = RegistrarUsuarioGym.objects.all().order_by('-id')
    UserDayList = RegistrarUsuarioGymDay.objects.all().order_by('-id')

    now = timezone.now()
    month = now.month
    year = now.year

    #Calculamos el numero de miembros 
    num_miembros = RegistrarUsuarioGym.objects.count()

    #Filtramos los miembros del gimnasio registrados en el mes
    miembros_mes = RegistrarUsuarioGym.objects.filter(dateInitial__month=month, dateInitial__year=year)
    #Cantidad de dinero miembros mensualidad
    total_gym_mes = sum(user.price for user in miembros_mes)

    #Filtramos los miembros del gimnasio registrados en el mes
    miembrosDay_mes = RegistrarUsuarioGymDay.objects.filter(dateInitial__month=month, dateInitial__year=year)
    #Cantidad de dinero del dia
    total_day_mes = sum(user.price for user in miembrosDay_mes)

    #Cantidad de dinero del mes
    total_month = total_gym_mes + total_day_mes

    #Filtramos los miembros registrados en el mes actual
    miembros_mes = RegistrarUsuarioGym.objects.filter(dateInitial__month=month, dateInitial__year=year).count()

    #Total de dinero en el gym
    total_gym = sum(user.price for user in UserGymList)
    total_day = sum(user.price for user in UserDayList)
    total = total_gym + total_day                                                     

    return render(request, 'welcome.html', { 
        'num_miembros': num_miembros, 
        'total_month': total_month, 
        'miembros_mes': miembros_mes,
        'total': total
        })

#@login_required
def listUser(request):
    userGymList = RegistrarUsuario.objects.all().order_by('-id')

    return render(request, 'login/listUser.html', {'userGymList': userGymList})


#Esta parte es la vista de los usuarios del gym
@login_required
def formcheckinGym(request):
    #Obtenemos la fecha actual
    today_date = date.today() 

    if request.method == 'GET':
        return render(request, 'registrarMiembros/checkInGym.html', { 'today_date': today_date})
    
    else:
        form = UsuarioFormGym(request.POST)

        if form.is_valid():
          usuario = form.save() #Guardamos el usuario si el formulario es valido
          return redirect('welcome')
        
    return render(request, 'registrarMiembros/checkInGym.html', { 'error': 'Usuario ya existe', 'today_date': today_date})

@login_required
def delete_user(request,id):
    usuarioGym= RegistrarUsuarioGym.objects.get(id=id)
    
    usuarioGym.delete()
    
    return redirect('welcome')

@login_required
def update_user(request, id):
    usuario= RegistrarUsuarioGym.objects.get(id=id)
    
    fecha_incorrecta = usuario.dateInitial.strftime("%m-%d-%Y")
    fecha_correcta = datetime.strptime(fecha_incorrecta, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateInitial = fecha_correcta

    fecha_incorrecta2 = usuario.dateFinal.strftime("%m-%d-%Y")
    fecha_correcta2 = datetime.strptime(fecha_incorrecta2, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateFinal = fecha_correcta2

    return render(request,'registrarMiembros/update.html', {'user': usuario})

@login_required
def actualizar(request, id):
    
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        address = request.POST['address']
        dateInitial = request.POST['dateInitial']
        dateFinal = request.POST['dateFinal']

        usuario= RegistrarUsuarioGym.objects.get(id=id)
        usuario.name = name
        usuario.lastname = lastname
        usuario.phone = phone
        usuario.address = address
        usuario.dateInitial = dateInitial
        usuario.dateFinal = dateFinal
        usuario.save()
        return redirect('welcome')

@login_required
def renovar_mensualidad(request, usuario_id=None):
    usuario = get_object_or_404(RegistrarUsuarioGym, id=usuario_id) #Obtenemos al usuario por su ID

    today_date = timezone.now().date() #Obtenemos la fecha actual

    if request.method == 'POST':
        #Crear el formulario apartir de los datos POST
        fecha_renovacion = request.POST.get('fechaRenovacion')
        fecha_vencimiento = request.POST.get('fechaVencimiento')

        if fecha_renovacion and fecha_vencimiento:
            nueva_renovacion = Renovacion(
                usuarioGym=usuario,
                fechaRenovacion=fecha_renovacion,
                fechaVencimiento=fecha_vencimiento
            )
            nueva_renovacion.save() #Guardamos la renovacion

            return redirect('welcome')           
        
    else:
        #Si es un GET, solo se muestra el form vacio 
        form = RenovacionForm(initial={'fecha_inicio': date.today()})
        return render(request, 'renovar_mensualidad.html', {
            'usuario': usuario,
            'today_date': today_date,
        })

#Esta es la parte de los usuarios de dia de rutina
@login_required
def formcheckinGymDay(request):
    #Obtenemos la fecha actual
    today_date = date.today()
    if request.method == 'GET':
        return render(request, 'registrarDiarios/checkIn.html', { 'today_date': today_date })
    
    else:
        form = UsuarioFormGymDay(request.POST)
        if form.is_valid():
          usuario = form.save()
          return redirect('welcome')
        
    return render(request, 'registrarDiarios/checkIn.html', { 'error': 'Error al guardar el usuario', 'today_date': today_date})

#@login_required
def listMember(request):
     # Obtener todos los usuarios
    UserGymList = RegistrarUsuarioGym.objects.all().order_by('-id')
    UserDayList = RegistrarUsuarioGymDay.objects.all().order_by('-id')
    
    # Obtener el template a usar
    template_type = request.GET.get('type', 'monthly')
    
    if template_type == 'monthly':
        template_name = 'registrarMiembros/listUserGym.html'
        #total_price = sum(user.price for user in UserGymList)
        context = {'userGym': UserGymList}
    else:
        template_name = 'registrarDiarios/listUserDay.html'
        total_price = sum(user.price for user in UserDayList)
        context = {'userGym': UserDayList, 'total_price': total_price}
    
    return render(request, template_name, context)

@login_required
def delete_userDay(request,id):
    usuarioGym= RegistrarUsuarioGymDay.objects.get(id=id)
    
    usuarioGym.delete()
    
    return redirect('welcome')

@login_required
def update_userDay(request, id):
    usuario= RegistrarUsuarioGymDay.objects.get(id=id)
    
    fecha_incorrecta = usuario.dateInitial.strftime("%m-%d-%Y")
    fecha_correcta = datetime.strptime(fecha_incorrecta, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateInitial = fecha_correcta

    return render(request,'registrarDiarios/updateDay.html', {'userDay': usuario})

@login_required
def actualizarDay(request, id):
    
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        dateInitial = request.POST['dateInitial']
        price = request.POST['price']

        usuario= RegistrarUsuarioGymDay.objects.get(id=id)
        usuario.name = name
        usuario.lastname = lastname
        usuario.phone = phone
        usuario.price = price

        usuario.dateInitial = dateInitial        
        usuario.save()
        return redirect('welcome')

#Historial de usuarios del gym
# def perfil_usuario(request, usuario_id):
#     usuario = get_object_or_404(RegistrarUsuarioGym, id=usuario_id)
#     renovaciones = Renovacion.objects.filter(usuario=usuario).order_by('-fecha_inicio')
#     return render(request, 'perfil_usuario.html', {'usuario': usuario, 'renovaciones': renovaciones})
