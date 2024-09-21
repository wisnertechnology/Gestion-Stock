# cartouches/forms.py
from django import forms
from .models import Commande, Demande, Distribution
from .models import CartoucheModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Si vous avez besoin de créer des instances de CartoucheModel de manière indépendante
class CartoucheModelForm(forms.ModelForm):
    class Meta:
        model = CartoucheModel
        fields = ['nom', 'stock_actuel', 'date_derniere_commande']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la cartouche'}),
            'stock_actuel': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock actuel'}),
            'date_derniere_commande': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }





class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['cartouche_model', 'quantite_commande', 'date_commande', 'date_reception']
        widgets = {
            'cartouche_model': forms.Select(attrs={'class': 'form-control'}),
            'quantite_commande': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité commandée'}),
            'date_commande': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_reception': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['departement', 'cartouche_model', 'quantite_demandee', 'nom_demandeur', 'code_demandeur']
        widgets = {
            'departement': forms.Select(attrs={'class': 'form-control'}),  # Liste déroulante pour les départements
            'cartouche_model': forms.Select(attrs={'class': 'form-control'}),  # Liste déroulante pour les modèles de cartouches
            'quantite_demandee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité demandée'}),
            'nom_demandeur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du demandeur'}),
            'code_demandeur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code du demandeur'}),
        }

class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['demande', 'quantite_distribuee']# je retire la valeur 'date_distribution'
        widgets = {
            'demande': forms.Select(attrs={'class': 'form-control'}),
            'quantite_distribuee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité distribuée'}),
            # 'date_distribution': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
#                                                 POUR LOGIN REGISTER
class FormulaireUtilisateur(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Pierre@gmail.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
        }
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }