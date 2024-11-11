from django.urls import path
from .views import formcheckinUser, Login, singoff, welcome, delete_user, update_user, actualizar, formcheckinGym, formcheckinGymDay, update_userDay, actualizarDay, delete_userDay, renovar_mensualidad, listUser



urlpatterns = [
    path('', Login, name='login'),
    path('checkinUser/', formcheckinUser, name='checkinUser'),
    path('logout/', singoff, name='logout'),
    path('welcome/', welcome, name='welcome'),
    path('listUser/', listUser, name='listUser'),

    path('update/<int:id>', update_user, name='update'),
    path('updateUsers/<int:id>', actualizar, name='updateUsers'),

    path('delete/<int:id>', delete_user, name='delete'),

    path('checkinGym/', formcheckinGym, name='checkinGym'),

    path('checkinDay/', formcheckinGymDay, name='checkinDay'),
    path('updateDay/<int:id>', update_userDay, name='updateDay'),
    path('updateUserDay/<int:id>', actualizarDay, name='updateUserDay'),
    path('deleteDay/<int:id>', delete_userDay, name='deleteDay'),
    
    path('renovarGym/<int:usuario_id>/', renovar_mensualidad, name='renovarGym'),

]