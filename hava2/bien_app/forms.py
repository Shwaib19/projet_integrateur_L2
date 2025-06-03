from django import forms
from .models import Propriete, Image

class ProprieteForm(forms.ModelForm):
    class Meta:
        model = Propriete
        fields = ['type', 'usage', 'statut', 'localisation', 'superficie', 'prix', 'option']

# Formulaire pour 5 images
class ImageUploadForm(forms.Form):
    image1 = forms.ImageField(
        required=True,
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
