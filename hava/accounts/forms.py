from django import forms
from .models import Utilisateur,Client,Agent,Bailleur
from django.contrib.auth.hashers import make_password

#Formulaire pour recuperer les infos tout en s'assurant du typage

#Client
class ClientForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe"
    )

    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'telephone', 'adresse']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
        }

    def save(self, commit=True):
        Client = super().save(commit=False)
        # Hasher le mot de passe avant d'enregistrer
        Client.mot_de_passe = make_password(self.cleaned_data['mot_de_passe'])
        if commit:
            Client.save()
        return Client
    
#Agent
class AgentForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label="mot_de_passe"
    )

    class Meta:
        model = Agent
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'telephone', 'adresse']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
        }

    def save(self, commit=True):
        Agent = super().save(commit=False)
        # Hasher le mot de passe avant d'enregistrer
        Agent.mot_de_passe = make_password(self.cleaned_data['mot_de_passe'])
        if commit:
            Agent.save()
        return Agent