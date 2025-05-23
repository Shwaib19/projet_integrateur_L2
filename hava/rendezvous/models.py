from django.db import models
from accounts.models import Agent, Client  # à adapter selon ton organisation
from propriete.models import Propriete  # idem

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]

    date = models.DateField()
    heure = models.TimeField()
    
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='rendez_vous')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='rendez_vous')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rendez_vous')

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"RDV {self.date} à {self.heure} - {self.client} avec {self.agent}"
