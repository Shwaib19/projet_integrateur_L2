from django.shortcuts import render, get_object_or_404, redirect
from .models import Propriete
from .forms import ProprieteForm, ImageUploadForm
from .models import Image
from django.contrib.auth.decorators import login_required
from .models import Propriete
from auth_app.models import ClientProfile
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def propriete_detail(request, pk):
    propriete = get_object_or_404(Propriete, pk=pk)
    images = propriete.images.all()
    
    est_favori = False
    if request.user.is_authenticated:
        try:
            profil = ClientProfile.objects.get(user=request.user)
            est_favori = propriete in profil.favoris.all()
            print(est_favori)
        except ClientProfile.DoesNotExist:
            est_favori = False

    return render(request, 'bien/detail.html', {
        'propriete': propriete,
        'images': images,
        'est_favori': est_favori
    })

def ajouter_propriete(request):
    if request.method == 'POST':
        prop_form = ProprieteForm(request.POST)
        img_form = ImageUploadForm(request.POST, request.FILES)
        print("fff")
        if prop_form.is_valid(): print("valid")
        if prop_form.is_valid() and img_form.is_valid():
            propriete = prop_form.save()
            
            for img_field in ['image1', 'image2', 'image3', 'image4', 'image5']:
                image_file = img_form.cleaned_data.get(img_field)
                if image_file:
                    Image.objects.create(propriete=propriete, image=image_file)

            return redirect('index')

    else:
        prop_form = ProprieteForm()
        img_form = ImageUploadForm()

    return render(request, 'bien/ajouter.html', {
        'prop_form': prop_form,
        'img_form': img_form,
    })
    
    
@login_required
@require_POST
def toggle_favori(request, propriete_id):
    propriete = get_object_or_404(Propriete, id=propriete_id)

    try:
        profil = ClientProfile.objects.get(user=request.user)
    except ClientProfile.DoesNotExist:
        return JsonResponse({'error': 'Seule les comptes clients ont le droit d\'aimer des propriétés'}, status=400)

    if propriete in profil.favoris.all():
        profil.favoris.remove(propriete)
        status = 'retirée'
    else:
        profil.favoris.add(propriete)
        status = 'ajoutée'

    return JsonResponse({
        'message': f'Propriété {status} des favoris.',
        'favoris_status': status
    })
    
 


@login_required
def liste_favoris(request):
    try:
        profil = ClientProfile.objects.get(user=request.user)
        favoris = profil.favoris.all()
    except ClientProfile.DoesNotExist:
        favoris = []
    return render(request, 'bien/favoris.html', {
        'proprietes': favoris
    })
