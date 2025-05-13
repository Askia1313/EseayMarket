from django.db import models
from authentification.models import Utilisateur
# Create your models here. 


class Boutique(models.Model):
    vendeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='boutiques/logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slogan = models.CharField(max_length=100, null=True, blank=True,default='')        
    adresse = models.TextField()
    contact = models.CharField(max_length=100, null=True, blank=True,default='')
    latitude = models.FloatField()
    longitude = models.FloatField()
    template_choisi = models.CharField(max_length=100,default='default')
    date_creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  
    date_activation = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.nom


class Produit(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/')
    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nom} ({self.boutique.nom})"

#class Commande(models.Model):
    #client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    #boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    #livreur = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'livreur'})
    #prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    #statut = models.CharField(max_length=50, choices=[('en_attente', 'En attente'), ('en_livraison', 'En livraison'), ('livree', 'Livrée')], default='en_attente')
    #adresse_livraison = models.TextField()
    #code_postal = models.CharField(max_length=10)
    #latitude = models.FloatField()
    #longitude = models.FloatField()
    #date_commande = models.DateTimeField(auto_now_add=True)
    #prix_livraison = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    #def __str__(self):
        #return f"Commande #{self.id} - {self.client}"


#class LigneCommande(models.Model):
    #commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    #produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    #quantite = models.PositiveIntegerField()

    #def __str__(self):
        #return f"{self.produit.nom} x{self.quantite}"

#class LikeBoutique(models.Model):
    #utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    #boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    #date = models.DateTimeField(auto_now_add=True)

#class LikeProduit(models.Model):
    #utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    #produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    #date = models.DateTimeField(auto_now_add=True)


#class Notification(models.Model):
    #utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    #message = models.TextField()
    #lu = models.BooleanField(default=False)
    #date = models.DateTimeField(auto_now_add=True)

#class LivreurBoutique(models.Model):
    #livreur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'livreur'})
    #boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    #est_externe = models.BooleanField(default=False)  # False = livreur de la boutique

    #def __str__(self):
        #return f"{self.livreur} - {self.boutique}"

