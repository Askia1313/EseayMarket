from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BoutiqueForm, ProduitForm
from django.contrib import messages
from vendeur.models import Boutique, Produit

@login_required
def creer_boutique(request):
    if request.method == 'POST':
        form = BoutiqueForm(request.POST, request.FILES)
        if form.is_valid():
            print("Utilisateur connecté :", request.user, type(request.user))
            boutique = form.save(commit=False)
            boutique.vendeur = request.user
            boutique.save()
            messages.success(request, "Votre demande de création de boutique a bien été enregistrée. Un administrateur va vous recontacter après validation.")
            return redirect('authentification:home')  
    else:
        form = BoutiqueForm()
    return render(request, 'creationBoutique.html', {'form': form})

@login_required
def ma_boutique(request):
    boutique = get_object_or_404(Boutique, vendeur=request.user)
    produits = Produit.objects.filter(boutique=boutique)
    return render(request, 'maBoutique.html', {'boutique': boutique, 'produits': produits})

@login_required
def ajouter_produit(request):
    boutique = get_object_or_404(Boutique, vendeur=request.user)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.boutique = boutique
            produit.save()
            messages.success(request, "Produit ajouté avec succès.")
        else:
            messages.error(request, "Erreur lors de l'ajout du produit.")
    return redirect('vendeur:ma_boutique')

@login_required
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, boutique__vendeur=request.user)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès.")
        else:
            messages.error(request, "Erreur lors de la modification du produit.")
        return redirect('vendeur:ma_boutique')
    # (optionnel : afficher un formulaire de modification en GET)
    return redirect('vendeur:ma_boutique')

@login_required
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, boutique__vendeur=request.user)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Produit supprimé avec succès.")
    return redirect('vendeur:ma_boutique')

@login_required
def toggle_disponibilite(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, boutique__vendeur=request.user)
    if request.method == 'POST':
        produit.disponible = not produit.disponible
        produit.save()
        messages.success(request, "Disponibilité du produit modifiée.")
    return redirect('vendeur:ma_boutique')