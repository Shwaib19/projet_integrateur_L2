# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, AgentProfile, ClientProfile
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST



def auth_view(request):
    """
    Vue unique pour connexion et inscription
    """
    # Si l'utilisateur est déjà connecté, le rediriger
    if request.user.is_authenticated:
        return redirect_by_user_type(request.user)
    
    # Initialiser les formulaires
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        # Déterminer quel formulaire a été soumis
        if 'login_submit' in request.POST:
            # Formulaire de connexion
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name()}!')
                return redirect_by_user_type(user)
            else:
                messages.error(request, 'Erreur de connexion. Vérifiez vos informations.')
        
        elif 'register_submit' in request.POST:
            # Formulaire d'inscription
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                messages.success(request, f'Inscription réussie! Bienvenue {user.get_full_name()}!')
                # Connecter automatiquement l'utilisateur après inscription
                login(request, user)
                return redirect_by_user_type(user)
            else:
                messages.error(request, 'Erreur lors de l\'inscription. Vérifiez les informations.')
    
    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    
    return render(request, 'accounts/index.html', context)

def redirect_by_user_type(user):
    """
    Redirige selon le type d'utilisateur
    """
    if user.user_type == 'MANAGER':
        return redirect('manager_dashboard')
    elif user.user_type == 'AGENT':
        return redirect('agent_dashboard')
    elif user.user_type == 'CLIENT':
        return redirect('index')
    else:
        return redirect('accounts:dashboard')

@login_required
def logout_view(request):
    """
    Déconnexion
    """
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    return redirect('index')

@login_required
def dashboard_view(request):
    """
    Tableau de bord général
    """
    context = {
        'user': request.user,
    }
    return render(request, 'welcome/index.html', context)

@login_required
def manager_dashboard(request):
    """
    Tableau de bord manager
    """
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('accounts:dashboard')
    
    agents = CustomUser.objects.filter(user_type='AGENT')
    clients = CustomUser.objects.filter(user_type='CLIENT')
    
    context = {
        'user': request.user,
        'agents': agents,
        'clients': clients,
        'agents_count': agents.count(),
        'clients_count': clients.count(),
    }
    
    return render(request, 'accounts/manager_dashboard.html', context)

@login_required
def agent_dashboard(request):
    """
    Tableau de bord agent
    """
    if request.user.user_type != 'AGENT':
        messages.error(request, 'Accès non autorisé.')
        return redirect('accounts:dashboard')
    
    # Récupérer le profil agent
    try:
        agent_profile = AgentProfile.objects.get(user=request.user)
    except AgentProfile.DoesNotExist:
        agent_profile = None
        messages.warning(request, 'Votre profil agent n\'est pas configuré.')
    
    # Récupérer les clients de cet agent
    my_clients = CustomUser.objects.filter(
        clientprofile__agent=request.user
    )
    
    context = {
        'user': request.user,
        'agent_profile': agent_profile,
        'my_clients': my_clients,
        'clients_count': my_clients.count(),
    }
    
    return render(request, 'accounts/agent_dashboard.html', context)

@login_required
def client_dashboard(request):
    """
    Tableau de bord client
    """
    if request.user.user_type != 'CLIENT':
        messages.error(request, 'Accès non autorisé.')
        return redirect('client:index')
    
    # Récupérer le profil client
    try:
        client_profile = ClientProfile.objects.select_related('agent').get(user=request.user)
    except ClientProfile.DoesNotExist:
        client_profile = None
        messages.warning(request, 'Votre profil client n\'est pas configuré.')
    
    context = {
        'user': request.user,
        'client_profile': client_profile,
        'assigned_agent': client_profile.agent if client_profile else None,
    }
    
    return render(request, 'welcome/index.html', context)

@login_required
def manage_user(request):
    User = get_user_model()  # récupère le modèle utilisateur actif
    utilisateurs = User.objects.all().values(
        'first_name', 'last_name', 'email', 'phone', 'user_type', 'date_joined'
    )

    return render(request, 'accounts/manager_user.html', {
        'utilisateurs': utilisateurs
    })
    
    
    


User = get_user_model()


def delete_user(request, email):
    user = get_object_or_404(User, email=email)
    if request.user == user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('manage_users')

    user.delete()
    messages.success(request, f"L'utilisateur {user.email} a été supprimé avec succès.")
    return redirect('manage_users')  # Assure-toi que cette URL existe