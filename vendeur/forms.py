from django import forms
from .models import Boutique, Produit

class BoutiqueForm(forms.ModelForm):
    class Meta:
        model = Boutique
        fields = ['nom', 'logo', 'contact', 'description', 'slogan', 'adresse', 'latitude', 'longitude', 'template_choisi']
        widgets = {
            'vendeur': forms.HiddenInput(),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la boutique'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slogan'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
        }



class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'stock', 'image', 'disponible']