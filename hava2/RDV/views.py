# app_rdv/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import DemandeRendezVousForm ,ConfirmationRendezVousForm
from .models import RendezVous
from bien_app.models import Propriete
from auth_app.models import ClientProfile  # selon ton organisation

@login_required
def prendre_rendez_vous(request, propriete_id):
    propriete = get_object_or_404(Propriete, id=propriete_id)


    if not hasattr(request.user, 'clientprofile'):
        return redirect('index')

    client = request.user
    client_profile = client.clientprofile

    
    if not client_profile.agent:
        messages.error(request, "Aucun agent ne vous a été assigné pour l’instant.")
        return redirect('index')

    agent = client_profile.agent.agentprofile

    if request.method == 'POST':
        form = DemandeRendezVousForm(request.POST)
        
        if form.is_valid():
            print("is valid")
            rdv = form.save(commit=False)
            rdv.client = client_profile
            rdv.agent = agent
            rdv.propriete = propriete
            rdv.save()
            messages.success(request, "Votre demande de rendez-vous a été envoyée à l’agent.")
            return redirect('mes_rdv')  # ou redirige vers les détails du bien
    else:
        form = DemandeRendezVousForm()

    return render(request, 'rdv/prendre_rdv.html', {
        'form': form,
        'propriete': propriete
    })

@login_required
def mes_rendez_vous(request):
    # Vérifie que l'utilisateur est un client
    if not hasattr(request.user, 'clientprofile'):
        messages.error(request, "Seuls les clients ont accès à cette page.")
        return redirect('index')  # ou une autre page d’accueil

    rendez_vous = RendezVous.objects.filter(client=request.user.clientprofile).order_by('-date_souhaitee')

    return render(request, 'rdv/mes_rdv.html', {
        'rendez_vous': rendez_vous
    })
    

def annuler_rendez_vous(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id, client=request.user.clientprofile)

    if rdv.statut == 'ANNULE':
        messages.warning(request, "Ce rendez-vous a déjà été annulé.")
    else:
        rdv.statut = 'ANNULE'
        rdv.save()
        messages.success(request, "Votre rendez-vous a été annulé avec succès.")

    return redirect('mes_rdv')


@login_required
def rendez_vous_agent(request):
    # Vérifie que l'utilisateur est un agent
    if not hasattr(request.user, 'agentprofile'):
        messages.error(request, "Seuls les agents peuvent accéder à cette page.")
        return redirect('index')  # ou autre vue

    # On récupère les RDV où l'agent est concerné
    rdvs = RendezVous.objects.filter(agent=request.user.agentprofile).order_by('-date_souhaitee')

    return render(request, 'rdv/mes_rdv.html', {
        'rendez_vous': rdvs
    })
    
@login_required
def modif_statut_rdv(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id)

    # Vérifie que l'utilisateur est bien un agent
    if not hasattr(request.user, 'agentprofile'):
        return redirect('index')

    if request.method == 'POST':
        form = ConfirmationRendezVousForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            messages.success(request, "Le statut du rendez-vous a été mis à jour avec succès.")
            return redirect('rdv_agent')  # Redirection adaptée à l'agent
    else:
        form = ConfirmationRendezVousForm(instance=rdv)

    return render(request, 'rdv/prendre_rdv.html', {
        'form': form,
        'rdv': rdv
    })