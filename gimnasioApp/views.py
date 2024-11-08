from django.shortcuts import render, redirect
from . forms import UsuarioForm, UsuarioFormGym, UsuarioFormGymDay
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .models import RegistrarUsuario, RegistrarUsuarioGym, RegistrarUsuarioGymDay
from django.contrib.auth.decorators import login_required

from datetime import datetime

import bcrypt  #esto nos sirve para encriptar la contraseña...ojo debemos instalarla pip install bcrypt 

# Create your views here.
#Esta parte es la vista de los usuarios que se loguean
def Login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    
    else:
        user = request.POST['user'] 
        password=request.POST['password']

        try:
            user_profile = RegistrarUsuario.objects.get(user=user)
        except RegistrarUsuario.DoesNotExist:
            return render(request, 'login/login.html', {'error': 'Username or password is incorrect'})
        
        #Verificamos la contraseña
        if bcrypt.checkpw(password.encode('utf-8'), user_profile.password.encode('utf-8')):
            #Guardamos la información en la sesión 
            request.session['user_name'] = f'{user_profile.name} {user_profile.lastname}'
            request.session['user_roles'] = f'{user_profile.roles}'
            return redirect('welcome')        
        else:
            return render(request, 'login/login.html', {'error': 'Username or password is incorrect'})
            

# @login_required
def registerBd(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            hashed_password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            usuario = form.save(commit=False)
            usuario.password= hashed_password.decode('utf-8') #Guardamos la contra como un string
            usuario.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'checkIn.html', {'form': form})

@login_required
def singoff(request):
    logout(request)
    return redirect('login')

#@login_required
def formcheckin(request):
    if request.method == 'GET':
        return render(request, 'login/checkInLogin.html')
    
    else:
        if request.POST['password'] == request.POST['repeatpassword']:
            try:
                user = User.objects.create_user(username=request.POST['user'], password=request.POST['password'])
                registerBd(request)
                user.save()
                login(request,user)
                return redirect('login')

            except IntegrityError:
                render(request, 'login/checkInLogin.html', { 'error': 'Usuario ya existe'}) 
        # return render(request, 'checkIn.html', { 'error': 'Error en el formulario'})
        
        return render(request, 'login/checkInLogin.html', { 'error': 'Password do not match'})    

#@login_required
def home(request):
    UserList = RegistrarUsuarioGym.objects.all()
    User = RegistrarUsuarioGymDay.objects.all()

    total_price = sum(user.price for user in User)
    
    return render(request, 'welcome.html', {'userGym': UserList, 'userDay': User, 'total_price': total_price})


#Esta parte es la vista de los usuarios del gym
#@login_required
def formcheckinGym(request):
    if request.method == 'GET':
        return render(request, 'checkInGym.html')
    
    else:
        form = UsuarioFormGym(request.POST)
        if form.is_valid():
          usuario = form.save()
          return redirect('welcome')
        
    return render(request, 'checkInGym.html', { 'error': 'Usuario ya existe'})

#@login_required
def delete_user(request,id):
    usuarioGym= RegistrarUsuarioGym.objects.get(id=id)
    
    usuarioGym.delete()
    
    return redirect('welcome')

#@login_required
def update_user(request, id):
    usuario= RegistrarUsuarioGym.objects.get(id=id)
    
    fecha_incorrecta = usuario.dateInitial.strftime("%m-%d-%Y")
    fecha_correcta = datetime.strptime(fecha_incorrecta, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateInitial = fecha_correcta

    fecha_incorrecta2 = usuario.dateFinal.strftime("%m-%d-%Y")
    fecha_correcta2 = datetime.strptime(fecha_incorrecta2, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateFinal = fecha_correcta2

    return render(request,'update.html', {'user': usuario})

#@login_required
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


#Esta es la parte de los usuarios de dia de rutina
#@login_required
def formcheckinGymDay(request):
    if request.method == 'GET':
        return render(request, 'checkIn.html')
    
    else:
        form = UsuarioFormGymDay(request.POST)
        if form.is_valid():
          usuario = form.save()
          return redirect('welcome')
        
    return render(request, 'checkIn.html', { 'error': 'Usuario ya existe'})

#@login_required
def delete_userDay(request,id):
    usuarioGym= RegistrarUsuarioGymDay.objects.get(id=id)
    
    usuarioGym.delete()
    
    return redirect('welcome')

#@login_required
def update_userDay(request, id):
    usuario= RegistrarUsuarioGymDay.objects.get(id=id)
    
    fecha_incorrecta = usuario.dateInitial.strftime("%m-%d-%Y")
    fecha_correcta = datetime.strptime(fecha_incorrecta, "%m-%d-%Y").strftime("%Y-%m-%d")
    usuario.dateInitial = fecha_correcta

    return render(request,'updateDay.html', {'userDay': usuario})

#@login_required
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
