# views.py
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from messenger.models import Discussion
from .models import CustomUser, AgentProfile, ClientProfile,BailleurProfile
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserInscriptionForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ClientModificationForm, CustomUserForm
from bien_app.models import Propriete
from RDV.models import RendezVous
from django.db.models import Q

def auth_view(request):
    if request.user.is_authenticated:
        return redirect_by_user_type(request.user)
    
    # Initialiser les formulaires
    login_form = CustomAuthenticationForm()
    register_form = CustomUserInscriptionForm()
    
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
    elif user.user_type == 'BAILLEUR':
        return redirect('mes_proprietes')
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
    elif request.user.user_type == 'BAILLEUR':
        return redirect('mes_proprietes')
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
    
    User_nb = CustomUser.objects.all().count()
    agents = CustomUser.objects.filter(user_type='AGENT').count()
    managers = CustomUser.objects.filter(user_type='MANAGER').count()
    clients = CustomUser.objects.filter(user_type='CLIENT').count()
    bailleurs = CustomUser.objects.filter(user_type='BAILLEUR').count()
    proprietes = Propriete.objects.all().count()

    
    context = {
        'user': request.user,
        'user_count': User_nb,
        'agents_count': agents,
        'clients_count': clients,
        'managers_count': managers,
        'bailleurs_count': bailleurs,
        'proprietes_count': proprietes, 
   
           
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
        ancien_agent = client.agent  # garder l'ancien agent avant save
        client_modifie = client_form.save(commit=False)
        nouvel_agent = client_modifie.agent

        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            if ancien_agent != nouvel_agent:
                # Vérifie s’il existe déjà une discussion entre le client et le nouvel agent
                discussion_existante = Discussion.objects.filter(
                    Q(client=client_modifie.user, agent=nouvel_agent.user) |
                    Q(agent=nouvel_agent.user, client=client_modifie.user)
                ).exists()
                
                if not discussion_existante:
                    # Crée une nouvelle discussion
                    Discussion.objects.create(
                        client=client_modifie.user,
                        agent=nouvel_agent.user
                    )
            return redirect('manage_users')  # ou autre redirection

    else:
        user_form = CustomUserForm(instance=user)
        client_form = ClientModificationForm(instance=client)

    return render(request, 'accounts/modifier.html', {
        'user_form': user_form,
        'client_form': client_form,
        'client_id': client_id,
    })
    
    
@login_required
def proprietes_du_bailleur(request):
    
    try:
        bailleur = request.user # via OneToOneField
        proprietes = Propriete.objects.filter(bailleur=bailleur)
    except BailleurProfile.DoesNotExist:
        proprietes = []

    return render(request, 'accounts/bailleur.html', {'proprietes': proprietes})


@login_required
def gestion_bailleurs(request):
    if request.user.user_type != "MANAGER":
        return redirect('index')

    # Optimisation des requêtes avec select_related et prefetch_related
    bailleurs = CustomUser.objects.filter(user_type="BAILLEUR").prefetch_related('proprietes')

    return render(request, 'accounts/gestion_bailleur.html', {
        'bailleurs': bailleurs,
    })


@login_required
def liste_rdv_agents(request):
    if request.user.user_type !="MANAGER":
        return redirect('index')

    rdvs_agents = RendezVous.objects.select_related('agent').order_by('-date_souhaitee')

    return render(request, 'RDV/mes_rdv.html', {
        'rendez_vous': rdvs_agents,
    })







##
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.db import models
from django.http import HttpResponse

##


from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg


@login_required
def generer_statistiques_pdf(request):
    # Vérification des permissions (ajustez selon vos besoins)
    if request.user.user_type not in ['MANAGER', 'ADMIN']:
        return HttpResponse('Accès non autorisé', status=403)

    # Calcul des statistiques
    total_props = Propriete.objects.count()
    total_vente = Propriete.objects.filter(option='vente').count()
    total_location = Propriete.objects.filter(option='location').count()
    
    total_bailleurs = CustomUser.objects.filter(user_type='BAILLEUR').count()
    total_agents = CustomUser.objects.filter(user_type='AGENT').count()
    total_clients = CustomUser.objects.filter(user_type='CLIENT').count()
    moyennes = Propriete.objects.aggregate(
    moyenne_vente=Avg('prix', filter=models.Q(option='vente')),
    moyenne_location=Avg('prix', filter=models.Q(option='location'))
)
    total_rdv = RendezVous.objects.count()
    rdv_confirmes = RendezVous.objects.filter(statut='CONFIRME').count()
    
    moyenne_prix = Propriete.objects.aggregate(Avg('prix'))['prix__avg'] or 0
    
    localisations = (
        Propriete.objects.values('localisation')
        .annotate(nombre=Count('id'))
        .order_by('-nombre')
    )

    context = {
        'stats': {
            'total_props': total_props,
            'total_vente': total_vente,
            'total_location': total_location,
            'total_bailleurs': total_bailleurs,
            'total_agents': total_agents,
            'total_clients': total_clients,
            'total_rdv': total_rdv,
            'rdv_confirmes': rdv_confirmes,
            'moyenne_prix': round(moyenne_prix, 2),
            'localisations': localisations,
            **moyennes
        },
        'user': request.user,
        'date_generation': timezone.now().strftime("%d/%m/%Y %H:%M"),
    }

    # Génération du PDF
    template = get_template('accounts/etat.html')
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)

    if not pdf.err:
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        # Nommage du fichier avec date/heure
        filename = f"rapport_{timezone.now().strftime('%Y-%m-%d')}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    return HttpResponse('Erreur lors de la génération du PDF', status=500)