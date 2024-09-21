from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render, redirect
from .models import CartoucheModel, Commande, Demande, Distribution
from .forms import CartoucheModelForm, CommandeForm, DemandeForm, DistributionForm, FormulaireUtilisateur
from django.http import HttpResponse
import pandas as pd

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages




# ----------------------------------------------------------------------------------
# Pour Acceuil
def home(request):
    return render(request, 'cartouches/index.html')
# ----------------------------------------------------------------------------------


# Pour Base
def base2(request):
    return render(request, 'cartouches/base2.html')
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
#                       POUR LOGIN REGISTER
def register(request):
    
    if request.method == 'POST':
        form = FormulaireUtilisateur(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vous compte a ete bien creer")
            return redirect('list_cartouches')
        else:
            messages.error(request, form.errors)
            # Afficher les erreurs dans la console pour diagnostic
            print(form.errors)
    else:
        form = FormulaireUtilisateur()
    return render(request, 'authentification/register.html', {'form':form})


def connection(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "Connexion reussie")
                return redirect('list_cartouches')
            else:
                messages.error(request, "erreur d'authentification")
        else:
                messages.error(request, "erreur d'authentification")
    form = AuthenticationForm()
    return render(request, 'authentification/login.html', {'form':form})

@login_required
def deconnection(request):
    logout(request)
    return redirect('home_name')














@login_required(login_url='connect_name')
def liste_cartouches(request):
    cartouches = CartoucheModel.objects.all()
    return render(request, 'cartouches/liste_cartouches_test.html', {'cartouches': cartouches})




# -------------------------------------------------------------------------------------
# POUR LA CREATION DES CARTOUCHES
@login_required(login_url='connect_name')
def ajouter_cartouche(request):
    if request.method == 'POST':
        form = CartoucheModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_cartouches')
    else:
        form = CartoucheModelForm()
    return render(request, 'cartouches/create_cartouche_test.html', {'form': form})

@login_required(login_url='connect_name')
def list_cartouches(request):
    cartouches = CartoucheModel.objects.all()
    return render(request, 'cartouches/list_cartouches_test.html', {'cartouches': cartouches})

@login_required(login_url='connect_name')
def update_cartouche(request, pk):
    cartouche = get_object_or_404(CartoucheModel, pk=pk)
    if request.method == 'POST':
        form = CartoucheModelForm(request.POST, instance=cartouche)
        if form.is_valid():
            form.save()
            return redirect('list_cartouches')
    else:
        form = CartoucheModelForm(instance=cartouche)
    return render(request, 'cartouches/update_cartouche_test.html', {'form': form})

@login_required(login_url='connect_name')
def detail_cartouche(request, pk):
    cartouche = get_object_or_404(CartoucheModel, pk=pk)
    return render(request, 'cartouches/detail_cartouche_test.html', {'cartouche': cartouche})

# ----------------------------------------------------------------------------------------

@login_required(login_url='connect_name')
def ajouter_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cartouches')
    else:
        form = CommandeForm()
    return render(request, 'cartouches/ajouter_commande_test.html', {'form': form})

@login_required(login_url='connect_name')
def ajouter_demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cartouches')
    else:
        form = DemandeForm()
    return render(request, 'cartouches/ajouter_demande_test.html', {'form': form})

@login_required(login_url='connect_name')
def ajouter_distribution(request):
    if request.method == 'POST':
        form = DistributionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cartouches')
    else:
        form = DistributionForm()
    return render(request, 'cartouches/ajouter_distribution_test.html', {'form': form})




def generer_rapport(request):
    # Récupérer les données de CartoucheModel
    cartouches = CartoucheModel.objects.all().values('nom', 'stock_actuel', 'date_derniere_commande')
    df_cartouches = pd.DataFrame(list(cartouches))
    
    # Récupérer les données de Commande
    commandes = Commande.objects.all().values('cartouche_model__nom', 'quantite_commande', 'date_commande', 'date_reception')
    df_commandes = pd.DataFrame(list(commandes))
    
    # Récupérer les données de Demande
    demandes = Demande.objects.all().values('departement', 'cartouche_model__nom', 'nom_demandeur', 'code_demandeur', 'quantite_demandee', 'date_demande', 'etat')
    df_demandes = pd.DataFrame(list(demandes))
    
    # Récupérer les données de Distribution
    distributions = Distribution.objects.all().values('demande__departement', 'demande__cartouche_model__nom', 'quantite_distribuee', 'date_distribution')
    df_distributions = pd.DataFrame(list(distributions))

    # Supprimer les fuseaux horaires des dates si présents
    for df in [df_cartouches, df_commandes, df_demandes, df_distributions]:
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns, UTC]':
                df[col] = pd.to_datetime(df[col], utc=True).dt.tz_localize(None)

    # Crée le fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rapport_tracabilite.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        # Écrire chaque DataFrame dans une feuille séparée
        df_cartouches.to_excel(writer, sheet_name='Cartouches', index=False)
        df_commandes.to_excel(writer, sheet_name='Commandes', index=False)
        df_demandes.to_excel(writer, sheet_name='Demandes', index=False)
        df_distributions.to_excel(writer, sheet_name='Distributions', index=False)

    return response

