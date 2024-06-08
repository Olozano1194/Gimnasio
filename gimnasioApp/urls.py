from django.urls import path
from .views import formcheckin, Login, singoff, home, delete_user, update_user, actualizar, formcheckinGym, formcheckinGymDay, update_userDay, actualizarDay, delete_userDay



urlpatterns = [
    path('', Login, name='login'),
    path('checkin/', formcheckin, name='checkin'),
    path('logout/', singoff, name='logout'),
    path('welcome/', home, name='welcome'),

    path('update/<int:id>', update_user, name='update'),
    path('updateUsers/<int:id>', actualizar, name='updateUsers'),

    path('delete/<int:id>', delete_user, name='delete'),

    path('checkinGym/', formcheckinGym, name='checkinGym'),

    path('checkinDay/', formcheckinGymDay, name='checkinDay'),
    path('updateDay/<int:id>', update_userDay, name='updateDay'),
    path('updateUserDay/<int:id>', actualizarDay, name='updateUserDay'),
    path('deleteDay/<int:id>', delete_userDay, name='deleteDay'),
    # path('listGym/', list_Gym, name='listGym'),

]