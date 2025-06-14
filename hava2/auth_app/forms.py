# forms.py
import random
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, AgentProfile, ClientProfile,BailleurProfile
from messenger.models import Discussion
class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé pour CustomUser (utilise email au lieu de username)
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro de téléphone (optionnel)'
        })
    )
    

    adresse = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse (optionnel)'
        })
    )
    
    user_type = forms.ChoiceField(
        required=False,
        choices= (
        ('CLIENT', 'Client'),
        ('AGENT', 'Agent'),
        ('BAILLEUR', 'Bailleur'),
        ('MANAGER', 'Manager'),
    ),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse (optionnel)'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'adresse','user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Supprimer le champ username du formulaire
        if 'username' in self.fields:
            del self.fields['username']
        
        # Personnalisation des widgets des mots de passe
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })

    def clean_email(self):
        """
        Vérifier que l'email n'existe pas déjà
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        """
        Sauvegarder l'utilisateur avec l'email comme username
        """
        user = super().save(commit=False)
        
        # Utiliser l'email comme username
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        
        if commit:
            user.save()
            # Créer automatiquement le profil selon le type d'utilisateur
            self.create_user_profile(user)
        
        return user


    def create_user_profile(self, user):
        """
        Créer automatiquement le profil selon le type d'utilisateur
        """
        if user.user_type == 'AGENT':
            AgentProfile.objects.get_or_create(user=user)

        elif user.user_type == 'BAILLEUR':
            created = BailleurProfile.objects.get_or_create(user=user)

        elif user.user_type == 'CLIENT':
            client_profile, created = ClientProfile.objects.get_or_create(user=user)

            if created:
                # Choix aléatoire d'un agent
                agents = CustomUser.objects.filter(user_type='AGENT')
                if agents.exists():
                    selected_agent = random.choice(agents)
                    
                    client_profile.agent = selected_agent
                    client_profile.save()

                    # 🔥 Obtenir le profil agent lié à l’utilisateur agent
                    try:
                        p_agent = selected_agent.agentprofile  # via OneToOneField
                    except AgentProfile.DoesNotExist:
                        p_agent = None
                    
                    if p_agent:
                        Discussion.objects.get_or_create(
                            id_client=client_profile,
                            id_agent=p_agent
                        )
        


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé utilisant l'email
    """
    username = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')  # Django utilise 'username' en interne
        password = self.cleaned_data.get('password')

        if email is not None and password:
            # Authentifier avec l'email
            self.user_cache = authenticate(
                self.request,
                username=email,  # On passe l'email comme username
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Email ou mot de passe incorrect.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ClientProfileForm(forms.ModelForm):
    """
    Formulaire pour le profil Client
    """
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Votre adresse',
            'rows': 3
        })
    )
    
    agent = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='AGENT'),
        required=False,
        empty_label="Sélectionner un agent (optionnel)",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = ClientProfile
        fields = ['address', 'agent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afficher les agents avec leur nom complet et email
        self.fields['agent'].queryset = CustomUser.objects.filter(
            user_type='AGENT'
        ).select_related()
        
        # Personnaliser l'affichage des choix d'agents
        choices = [('', 'Sélectionner un agent (optionnel)')]
        for agent in self.fields['agent'].queryset:
            display_name = f"{agent.get_full_name()} ({agent.email})"
            choices.append((agent.id, display_name))
        
        self.fields['agent'].choices = choices

class UserUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour des informations utilisateur
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_email(self):
        """
        Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre utilisateur.")
        return email
    
    def save(self, commit=True):
        """
        Sauvegarder avec synchronisation email/username
        """
        user = super().save(commit=False)
        
        # Synchroniser username avec email si l'email change
        if user.email != self.cleaned_data['email']:
            user.username = self.cleaned_data['email']
            user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user
    

class ClientModificationForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = ['agent']  # ou ajoute d’autres champs spécifiques si besoin

class CustomUserForm(forms.ModelForm):
    
    first_name = forms.CharField(
    max_length=30,
    label='Prenom',
    required=True,
    widget=forms.TextInput(attrs={
        'class': 'form-control'
    })
    )
    
    last_name = forms.CharField(
        max_length=30,
        label='Nom',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'adresse','phone']