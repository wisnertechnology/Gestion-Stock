# Generated by Django 5.1 on 2024-09-11 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartoucheModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('stock_actuel', models.PositiveIntegerField(default=0)),
                ('date_derniere_commande', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite_commande', models.PositiveIntegerField()),
                ('date_commande', models.DateField()),
                ('date_reception', models.DateField(blank=True, null=True)),
                ('cartouche_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartouches.cartouchemodel')),
            ],
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departement', models.CharField(choices=[('IT', 'IT'), ('Comptabilité', 'Comptabilité'), ('Sécurité', 'Sécurité'), ('Production', 'Production')], max_length=50)),
                ('quantite_demandee', models.PositiveIntegerField()),
                ('date_demande', models.DateTimeField(auto_now_add=True)),
                ('etat', models.CharField(default='En attente', max_length=20)),
                ('cartouche_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cartouches.cartouchemodel')),
            ],
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite_distribuee', models.PositiveIntegerField()),
                ('date_distribution', models.DateTimeField(auto_now_add=True)),
                ('demande', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cartouches.demande')),
            ],
        ),
    ]
