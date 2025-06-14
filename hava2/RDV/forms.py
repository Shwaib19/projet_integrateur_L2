from django import forms
from .models import RendezVous
from django.utils import timezone

# 🔹 1. Formulaire côté CLIENT — création de la demande
class DemandeRendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['date_souhaitee', 'commentaire_client']
        widgets = {
            'date_souhaitee': forms.DateInput(attrs={'type': 'date', 'class': 'form-control' ,'min': timezone.now().strftime('%Y-%m-%d')  }),
            'commentaire_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message à l’agent (facultatif)'}),
        }


# 🔹 2. Formulaire côté AGENT — confirmation du rendez-vous
class ConfirmationRendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['date_confirmee', 'commentaire_agent']
        widgets = {
            'date_confirmee': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control' ,'min': timezone.now().strftime('%Y-%m-%d')}),
            'commentaire_agent': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message pour le client (facultatif)'}),
        }

# 🔹 3. Formulaire minimal côté CLIENT pour validation finale (ou annulation)
class ValidationRendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = []  # On ne modifie que le statut dans la vue
