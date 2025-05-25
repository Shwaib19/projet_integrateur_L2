from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import  *
from django.contrib.auth import login
from accounts.models import Utilisateur


###
### Vues de creations de comptes
###



def register_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profil_utilisateur')
    else:
        form = ClientForm()
    return render(request, 'accounts/register.html', {'form': form})


#La creation des agent est exclusivement reserver au manager
#la creation d'un agent requiert d'etre connecté en tant que manager

@login_required
def register_agent(request):
    # Vérification du type Manager
    if request.user.type != 'Manager':
        raise PermissionDenied("Accès réservé aux managers")
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profil_utilisateur')
    else:
        form = AgentForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def register_bailleur(request):
    # Vérification du type Manager
    if request.user.type != 'Manager':
        raise PermissionDenied("Accès réservé aux managers")
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profil_utilisateur')
    else:
        form = AgentForm()
    return render(request, 'accounts/register.html', {'form': form})


###
### Vues de connexion et de connexion
###

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']

            try:
                utilisateur = Utilisateur.objects.get(email=email)
                if check_password(mot_de_passe, utilisateur.mot_de_passe):
                    # Stocker l'utilisateur en session
                    request.session['utilisateur_id'] = utilisateur.id
                    request.session['type_compte'] = utilisateur.type
                    messages.success(request, "Connexion réussie.")
                    #
                    #
                    return redirect('accueil')  ## À adapter selon ta route d'accueil
                ## utiliser un switch pour renvoie sur un page suivant le type du compte
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Aucun utilisateur trouvé avec cet email.")
    else:
        form = LoginForm()

    return render(request, "accounts/index.html", {"form": form})


def logout_view(request):
    # Supprimer toutes les données de session
    request.session.flush()
    messages.success(request, "Déconnexion réussie.")
    return redirect('login')  # Redirige vers la page de connexion