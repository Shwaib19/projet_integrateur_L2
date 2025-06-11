# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, AgentProfile, ClientProfile
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ClientModificationForm, CustomUserForm


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
                print("valide")
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
    
    
def redirect_user(request):
    """
    Redirige selon le type d'utilisateur
    """
    if request.user.user_type == 'MANAGER':
        return redirect('manager_dashboard')
    elif request.user.user_type == 'AGENT':
        return redirect('agent_dashboard')
    elif request.user.user_type == 'CLIENT':
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
        return redirect('redirect_user')
    
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
        return redirect('redirect_user')
    
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
        return redirect('redirect_user')
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
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    User = get_user_model()  # récupère le modèle utilisateur actif
    utilisateurs = User.objects.all().values(
        'first_name', 'last_name', 'email', 'phone', 'user_type', 'date_joined' ,'id'
    ).order_by('-date_joined')

    return render(request, 'accounts/manager_user.html', {
        'utilisateurs': utilisateurs
    })
    
    
    


User = get_user_model()


def delete_user(request, email):
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    user = get_object_or_404(User, email=email)
    if request.user == user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('manage_users')

    user.delete()
    messages.success(request, f"L'utilisateur {user.email} a été supprimé avec succès.")
    return redirect('manage_users')  # Assure-toi que cette URL existe

def manager_add_user(request):

    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        
        if 'register_submit' in request.POST:
            # Formulaire d'inscription
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                print("valide")
                user = register_form.save()
                
                messages.success(
                    request,
                    f"L'utilisateur {user.first_name} {user.last_name} a été créé avec succès."
                )
                
                return redirect("manage_users")

            
            else:
                messages.error(request, 'Erreur lors de l\'inscription. Vérifiez les informations.')
    
    context = {
        'register_form': register_form,
    }
    
    return render(request, 'accounts/manager_add_user.html', context)


login_required
def liste_agents(request):
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    agents = AgentProfile.objects.all()
    return render(request, 'accounts/liste_agent.html', {'agents': agents})




def clients_par_agent(request, agent_id):
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    try:
        # Récupération du profil agent à partir de l'ID du user
        agent_profile = AgentProfile.objects.get(user__id=agent_id)
        # Récupération des clients liés à ce user (qui est un agent)
        clients = ClientProfile.objects.filter(agent=agent_profile.user)
        
        data = [
            {
                'nom': c.user.last_name,
                'prenom': c.user.first_name,
                'email': c.user.email,
                'id': c.user.id
            }
            for c in clients
        ]
        return JsonResponse({'clients': data})
    except AgentProfile.DoesNotExist:
        return JsonResponse({'clients': []})
    
    
def retirer_client(request, client_id):
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    try:
        client = ClientProfile.objects.get(user__id=client_id)
        client.agent = None  # On supprime l'affectation à un agent
        client.save()
        return JsonResponse({'success': True, 'message': 'Client retiré de l’agent'})
    except ClientProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Client introuvable'})


def modifier_client(request, client_id):
    
    if request.user.user_type != 'MANAGER':
        messages.error(request, 'Accès non autorisé.')
        return redirect('redirect_user')
    
    
    client = get_object_or_404(ClientProfile, user__id=client_id)
    
    user = client.user

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        client_form = ClientModificationForm(request.POST, instance=client)

        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            return redirect('manage_users')  # ou autre redirection

    else:
        user_form = CustomUserForm(instance=user)
        client_form = ClientModificationForm(instance=client)

    return render(request, 'accounts/modifier.html', {
        'user_form': user_form,
        'client_form': client_form,
        'client_id': client_id,
    })