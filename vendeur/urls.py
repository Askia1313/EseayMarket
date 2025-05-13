from django.urls import path
from . import views

app_name = 'vendeur'
urlpatterns = [
    path('creer-boutique/', views.creer_boutique, name='creer_boutique'),
    path('ma-boutique/', views.ma_boutique, name='ma_boutique'),
    path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier-produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('toggle-disponibilite/<int:produit_id>/', views.toggle_disponibilite, name='toggle_disponibilite'),
]