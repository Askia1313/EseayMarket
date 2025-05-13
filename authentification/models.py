from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------------------------
# UTILISATEUR
# ---------------------------
class Utilisateur(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    ROLES = (
        ('client', 'Client'),
        ('vendeur', 'Vendeur'),
        ('livreur', 'Livreur'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES,default='client')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
