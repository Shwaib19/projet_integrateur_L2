from django.db import models
from accounts.models import Agent, Client,Utilisateur

class Discussion(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='discussions')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='discussions')
    date_debut = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion entre {self.client} et {self.agent}"

class Message(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    expediteur = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages_recus')

    def __str__(self):
        return f"De {self.expediteur} à {self.destinataire} le {self.date_envoi}"