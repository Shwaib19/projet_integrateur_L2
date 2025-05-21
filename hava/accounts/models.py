from django.db import models

# Classe mère abstraite Utilisateur
class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    type = models.CharField(max_length=50, editable=False)

    class Meta:
        abstract = True
        
        ### puisse que utilisateur est abstrait il ne sera instancier que lors de l'instanciation d'un de ses filles
        ### donc a sa sauvegarde type prendra la valeur du nom de la sous classe qui la specialisé
    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.__class__.__name__.lower()
        super().save(*args, **kwargs)

# Client
class Client(Utilisateur):
    
    liste_favoris = models.ManyToManyField('Propriete', blank=True)

# Bailleur
class Bailleur(Utilisateur):
    # les propriétés seront reliées via un champ ForeignKey dans le modèle Propriete
    pass

# Agent
class Agent(Utilisateur):
    clients = models.ManyToManyField('Client', related_name='agents_suivi', blank=True)

# Manager
class Manager(Utilisateur):
    pass
