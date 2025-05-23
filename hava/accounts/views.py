from django.shortcuts import render, redirect
from .models import Utilisateur
from .forms import UtilisateurForm
from django.contrib.auth import authenticate, login

def register_client(request):
    if request.method == "POST":
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'CLIENT'  # 3🟢 correspond à ton modèle
            user.save()
            login(request, user)
            return redirect('profil_utilisateur')
    else:
        form = UtilisateurForm()
    return render(request, 'accounts/register.html', {'form': form})
