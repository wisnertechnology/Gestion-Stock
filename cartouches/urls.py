from django.urls import path
from .views import deconnection, connection, register, base2, home, detail_cartouche ,update_cartouche ,ajouter_cartouche, list_cartouches, liste_cartouches, ajouter_commande, ajouter_demande, ajouter_distribution, generer_rapport

urlpatterns = [
    path('', home, name='home_name'),

    path('base2', base2, name='base2_name'),

    # LOGIN & REGISTER &
    path('register', register, name='register_name'),
    path('connection', connection, name='connect_name'),
    path('deconnection', deconnection, name='disconnect_name'),


    path('list', liste_cartouches, name='liste_cartouches'),
    path('cartouche/ajouter/', ajouter_cartouche, name='ajouter_cartouche'),
    path('cartouches/', list_cartouches, name='list_cartouches'),
    path('cartouche/update/<int:pk>/', update_cartouche, name='update_cartouche'),
    path('cartouche/<int:pk>/', detail_cartouche, name='detail_cartouche'),

    path('commande/ajouter/', ajouter_commande, name='ajouter_commande'),
    path('demande/ajouter/', ajouter_demande, name='ajouter_demande'),
    path('distribution/ajouter/', ajouter_distribution, name='ajouter_distribution'),
    path('rapport/', generer_rapport, name='generer_rapport'),
]
