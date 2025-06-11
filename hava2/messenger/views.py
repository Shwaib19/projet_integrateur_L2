from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Discussion, Message
from auth_app.models import AgentProfile , ClientProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Max


@login_required
def liste_discussions_agent(request):
    try:
        agent = AgentProfile.objects.get(user=request.user)
    except AgentProfile.DoesNotExist:
        return redirect("index")

    # Récupère toutes les discussions de l’agent
    discussions = Discussion.objects.filter(id_agent=agent).prefetch_related('messages', 'id_client__user')
    
    discussions = Discussion.objects.annotate(
        Last_messages_date=Max('messages__date_envoi')
        ).order_by('-Last_messages_date')
    
    discussions_data = []
    for discussion in discussions:
        dernier_message = discussion.messages.order_by('-date_envoi').first()
        client_nom = discussion.id_client.user.get_full_name()
        
        discussions_data.append({
            'discussion': discussion,
            'dernier_message': dernier_message,
            'client_nom': client_nom,
        })

    return render(request, 'messenger/liste_discussions_agent.html', {
        'discussions_data': discussions_data,
    })





@login_required
def discussions_client(request):
    try:
        client = ClientProfile.objects.get(user=request.user)
    except client.DoesNotExist:
        return redirect("index")

    # Récupère toutes les discussions du client
    discussions = Discussion.objects.filter(id_client=client).prefetch_related('messages', 'id_agent__user')
        
    discussions_data = []
    for discussion in discussions:
        dernier_message = discussion.messages.order_by('-date_envoi').first()
        agent_nom = discussion.id_agent.user.get_full_name()
        
        discussions_data.append({
            'discussion': discussion,
            'dernier_message': dernier_message,
            'client_nom': agent_nom,
        })

    return render(request, 'messenger/liste_discussions_client.html', {
        'discussions_data': discussions_data,
    })




@login_required
def messages_discussion_json(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, id_agent__user=request.user)
    messages = discussion.messages.order_by('date_envoi').values(
        'id', 'contenu', 'date_envoi',
        'expediteur__first_name', 'destinataire__first_name'
    )
    
    return JsonResponse(list(messages), safe=False)


@login_required
def messages_discussion_json_client(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, id_client__user=request.user)
    messages = discussion.messages.order_by('date_envoi').values(
        'id', 'contenu', 'date_envoi',
        'expediteur__first_name', 'destinataire__first_name'
    )
    
    return JsonResponse(list(messages), safe=False)





@login_required
@require_POST
def envoyer_message(request, discussion_id):
    # Récupération optimisée avec select_related pour les relations ForeignKey
    discussion = get_object_or_404(
        Discussion.objects.select_related('id_agent__user', 'id_client__user'),
        id=discussion_id
    )
    print("eee")
    # Validation des données
    try:
        data = json.loads(request.body)
        contenu = data.get('contenu', '').strip()
        if not contenu:
            raise ValueError("Message vide")
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'error': 'Données JSON invalides'},
            status=400
        )
    except (AttributeError, ValueError) as e:
        return JsonResponse(
            {'success': False, 'error': str(e)},
            status=400
        )

    # Vérification d'autorisation plus concise
    expediteur = request.user
    if expediteur not in {discussion.id_agent.user, discussion.id_client.user}:
        return JsonResponse(
            {'success': False, 'error': 'Accès non autorisé'},
            status=403
        )

    # Détermination du destinataire
    destinataire = (
        discussion.id_client.user 
        if expediteur == discussion.id_agent.user 
        else discussion.id_agent.user
    )

    # Création et ajout du message en une seule requête
    message = Message.objects.create(
        discussion=discussion,  # Ajout recommandé si votre modèle le supporte
        contenu=contenu,
        expediteur=expediteur,
        destinataire=destinataire,
        date_envoi=timezone.now()
    )

    # Pas besoin de save() car create() le fait déjà
    # discussion.listeMessages.add(message)  # Redondant si discussion est ForeignKey

    return JsonResponse({
        'success': True,
        'message_id': message.id,  # Information utile pour le frontend
        'date_envoi': message.date_envoi.isoformat()
    })
    

