# models.py
from django.contrib.auth.models import AbstractUser
from bien_app.models import Propriete
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('CLIENT', 'Client'),
        ('AGENT', 'Agent'),
        ('MANAGER', 'Manager'),
        ('BAILLEUR', 'Bailleur'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="CLIENT" )
    adresse = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Rendre l'email unique et obligatoire
    email = models.EmailField(unique=True)
    
    # Utiliser l'email comme identifiant de connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Utilisateur"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class AgentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'AGENT'}
    )
    specialty = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Agent: {self.user.get_full_name()} ({self.user.email})"



class ClientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'CLIENT'}
    )
    agent = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'AGENT'},
        related_name='clients'
    )
    
    favoris = models.ManyToManyField(Propriete, related_name='favoris_clients', blank=True)
    
    def __str__(self):
        return f"Client: {self.user.get_full_name()} ({self.user.email})"
    



class BailleurProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'BAILLEUR'}
    )
    
    def __str__(self):
        return f"Bailleur: {self.user.get_full_name()} ({self.user.email})"