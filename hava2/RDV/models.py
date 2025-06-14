from django.db import models
from auth_app.models import AgentProfile, ClientProfile
from bien_app.models import Propriete
# Create your models here.
class RendezVous(models.Model):


    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='rdv_client')
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='rdv_agent')
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE)
    
    date_souhaitee = models.DateField()
    date_confirmee = models.DateField(null=True, blank=True,)
    
    statut = models.CharField(max_length=20, default='EN_ATTENTE')
    commentaire_client = models.TextField(blank=True)
    commentaire_agent = models.TextField(blank=True)

    def __str__(self):
        return f"{self.client} - {self.propriete} - {self.statut}"
