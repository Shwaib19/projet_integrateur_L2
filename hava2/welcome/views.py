from django.shortcuts import render
from bien_app.models import Propriete

def index(request):
    proprietes = Propriete.objects.all()
    return render(request, 'welcome/index.html', {
        'proprietes': proprietes
    })