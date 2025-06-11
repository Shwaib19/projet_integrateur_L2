from django.db import models
from django.conf import settings
from auth_app.models import AgentProfile , ClientProfile   # Adapte selon l'organisation de ton projet

class Discussion(models.Model):
    id_agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='discussions')
    id_client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='discussions')
    date_debut = models.DateTimeField(auto_now_add=True)  # Date de création automatique

    def __str__(self):
        return f"Discussion entre {self.id_client.user.get_full_name()} et {self.id_agent.user.get_full_name()}"


class Message(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_recus'
    )

    def __str__(self):
        return f"Message de {self.expediteur.get_full_name()} à {self.destinataire.get_full_name()}"
