from django import forms
from .models import Propriete, Image
from auth_app.models import CustomUser

class ProprieteForm(forms.ModelForm):
    
    bailleur = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='BAILLEUR'),
        required=False,
        empty_label="Sélectionner un bailleur (optionnel)",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    usage = forms.CharField(
        max_length=250,
        required=True,
        label="Usage et description",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = Propriete
        fields = ['type', 'usage', 'statut', 'localisation', 'superficie', 'prix', 'option','bailleur']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afficher les agents avec leur nom complet et email
        self.fields['bailleur'].queryset = CustomUser.objects.filter(
            user_type='BAILLEUR'
        ).select_related()
        
        self.fields['bailleur'].widget = forms.HiddenInput()
        
        # Personnaliser l'affichage des choix d'agents
        choices = [('', 'Sélectionner un Bailleur (optionnel)')]
        for bailleur in self.fields['bailleur'].queryset:
            display_name = f"{bailleur.get_full_name()} ({bailleur.email})"
            choices.append((bailleur.id, display_name))
        
        self.fields['bailleur'].choices = choices



class B_ProprieteForm(forms.ModelForm):
    
    bailleur = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='BAILLEUR'),
        required=False,
        empty_label="Sélectionner un bailleur (optionnel)",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Propriete
        fields = ['type', 'usage', 'statut', 'localisation', 'superficie', 'prix', 'option','bailleur']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afficher les agents avec leur nom complet et email
        self.fields['bailleur'].queryset = CustomUser.objects.filter(
            user_type='BAILLEUR'
        ).select_related()
        
        self.fields['bailleur'].widget = forms.HiddenInput()
        
        # Personnaliser l'affichage des choix d'agents
        choices = [('', 'Sélectionner un Bailleur (optionnel)')]
        for bailleur in self.fields['bailleur'].queryset:
            display_name = f"{bailleur.get_full_name()} ({bailleur.email})"
            choices.append((bailleur.id, display_name))
        
        self.fields['bailleur'].choices = choices



# Formulaire pour 5 images
class ImageUploadForm(forms.Form):
    image1 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'image1',
            'name': 'images',
            'onchange': 'previewImages(event)',
        })
    )
    image2 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'image2',
            'name': 'images',
            'onchange': 'previewImages(event)',
        })
    )
    image3 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'image3',
            'name': 'images',
            'onchange': 'previewImages(event)',
        })
    )
    image4 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'image4',
            'name': 'images',
            'onchange': 'previewImages(event)',
        })
    )
    image5 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'image5',
            'name': 'images',
            'onchange': 'previewImages(event)',
        })
    )
    # Continue jusqu'à image5...

