from django.shortcuts import render
from bien_app.models import Propriete

def index(request):
    proprietes = Propriete.objects.all().order_by('-id')
    return render(request, 'welcome/index.html', {
        'proprietes': proprietes
    })
def service(request):
    return render(request, 'welcome/service.html')

def contact(request):
    return render(request, 'welcome/contact.html')
def apropos(request):
    return render(request, 'welcome/apropos.html')