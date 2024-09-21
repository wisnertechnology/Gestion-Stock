from django.db import models

# Create your models here.
from django.db import models

class CartoucheModel(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    #unique=True : Ajouté au champ nom, cela assure l'unicité de chaque valeur dans ce champ, empêchant l'insertion de deux enregistrements avec le même nom.
    stock_actuel = models.PositiveIntegerField(default=0)
    date_derniere_commande = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    cartouche_model = models.ForeignKey(CartoucheModel, on_delete=models.CASCADE)
    quantite_commande = models.PositiveIntegerField()
    date_commande = models.DateField()
    date_reception = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.date_reception:
            self.cartouche_model.stock_actuel += self.quantite_commande
            self.cartouche_model.date_derniere_commande = self.date_reception
            self.cartouche_model.save()
        super().save(*args, **kwargs)

class Demande(models.Model):
    DEPARTEMENTS = [
        ('IT', 'IT'),
        ('Comptabilité', 'Comptabilité'),
        ('Sécurité', 'Sécurité'),
        ('Production', 'Production'),
    ]

    departement = models.CharField(max_length=50, choices=DEPARTEMENTS)
    cartouche_model = models.ForeignKey(CartoucheModel, on_delete=models.CASCADE)
    quantite_demandee = models.PositiveIntegerField()
    date_demande = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, default='En attente')
    nom_demandeur = models.CharField(max_length=100, default='Nom inconnu')  # Champ pour le nom de l'utilisateur qui fait la demande
    code_demandeur = models.CharField(max_length=50, default='123...')  # Champ pour le code ou identifiant de l'utilisateur


    def __str__(self):
        return f"Demande de {self.departement} pour {self.cartouche_model}"

# class Distribution(models.Model):
#     demande = models.OneToOneField(Demande, on_delete=models.CASCADE)
#     quantite_distribuee = models.PositiveIntegerField()
#     date_distribution = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.demande.cartouche_model.stock_actuel >= self.quantite_distribuee:
#             self.demande.cartouche_model.stock_actuel -= self.quantite_distribuee
#             self.demande.cartouche_model.save()
#         super().save(*args, **kwargs)

# models.py

class Distribution(models.Model):
    demande = models.OneToOneField(Demande, on_delete=models.CASCADE)
    quantite_distribuee = models.PositiveIntegerField()
    date_distribution = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Vérifie si le stock est suffisant pour la distribution
        if self.demande.cartouche_model.stock_actuel >= self.quantite_distribuee:
            # Réduit le stock actuel du modèle de cartouche
            self.demande.cartouche_model.stock_actuel -= self.quantite_distribuee
            self.demande.cartouche_model.save()
            
            # Met à jour l'état de la demande associée à "Distribuée"
            self.demande.etat = "Distribuée"
            self.demande.save()
        else:
            # Met à jour l'état de la demande à "Stock insuffisant" si le stock n'est pas suffisant
            self.demande.etat = "Stock insuffisant"
            self.demande.save()

        # Sauvegarde la distribution
        super().save(*args, **kwargs)

