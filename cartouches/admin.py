from django.contrib import admin
from .models import CartoucheModel, Commande, Demande, Distribution

# Register your models here.

@admin.register(CartoucheModel)
class CartoucheModelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'stock_actuel', 'date_derniere_commande')
    search_fields = ('nom',)
    list_filter = ('date_derniere_commande',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('cartouche_model', 'quantite_commande', 'date_commande', 'date_reception')
    search_fields = ('cartouche_model__nom',)
    list_filter = ('date_commande', 'date_reception')
    date_hierarchy = 'date_commande'

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('departement', 'cartouche_model', 'quantite_demandee', 'date_demande', 'etat', 'nom_demandeur', 'code_demandeur')
    search_fields = ('departement', 'cartouche_model__nom')
    list_filter = ('departement', 'etat', 'date_demande')
    date_hierarchy = 'date_demande'

@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('demande', 'quantite_distribuee', 'date_distribution')
    search_fields = ('demande__departement', 'demande__cartouche_model__nom')
    list_filter = ('date_distribution',)
    date_hierarchy = 'date_distribution'
