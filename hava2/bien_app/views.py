from django.shortcuts import render, get_object_or_404, redirect
from .models import Propriete
from .forms import ProprieteForm, ImageUploadForm
from .models import Image
from django.contrib.auth.decorators import login_required
from .models import Propriete
from auth_app.models import ClientProfile, BailleurProfile
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

@login_required
def ajouter_propriete(request):
    if request.method == 'POST':
        prop_form = ProprieteForm(request.POST)
        img_form = ImageUploadForm(request.POST, request.FILES)

        if prop_form.is_valid() and img_form.is_valid():
            if request.user.user_type == "BAILLEUR":
                propriete = prop_form.save(commit=False)
                propriete.bailleur = request.user
                propriete.save()

                # Enregistrer les images
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
    
 
from django.contrib import messages

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




@login_required
def modifier_propriete(request, pk):
    bailleur = getattr(request.user, 'bailleurprofile', None)
    if not bailleur:
        messages.error(request, "Vous devez être un bailleur pour modifier une propriété.")
        return redirect('mes_proprietes')

    propriete = get_object_or_404(Propriete, pk=pk, bailleur=bailleur.user)

    if request.method == 'POST':
        form = ProprieteForm(request.POST, request.FILES, instance=propriete)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            propriete_modifiee = form.save(commit=False)
            propriete_modifiee.bailleur = bailleur.user
            propriete_modifiee.save()

            # Traitement des nouvelles images
            for img_field in ['image1', 'image2', 'image3', 'image4', 'image5']:
                image_file = image_form.cleaned_data.get(img_field)
                if image_file:
                    image_obj = Image.objects.create(propriete=propriete_modifiee, image=image_file)
                    print("Image créée :", image_obj.image.url)
            messages.success(request, "Propriété modifiée avec succès.")
            return redirect('mes_proprietes')
        else:
            messages.error(request, "Une erreur est survenue. Veuillez corriger les champs du formulaire.")
            if not form.is_valid():
                print("Erreurs formulaire propriété:", form.errors)
            if not image_form.is_valid():
                print("Erreurs formulaire images:", image_form.errors)

    else:
        form = ProprieteForm(instance=propriete)
        image_form = ImageUploadForm()

    images_existantes = propriete.images.all()

    return render(request, 'bien/modifier.html', {
        'form': form,
        'image_form': image_form,
        'propriete': propriete,
        'images_existantes': images_existantes
    })

    
    

@login_required
def supprimer_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    bailleur = getattr(request.user, 'bailleurprofile', None)
    if image.propriete.bailleur != bailleur.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette image.")
        return redirect('mes_proprietes')

    image.delete()
    messages.success(request, "Image supprimée avec succès.")
    return redirect('modifier_propriete', pk=image.propriete.pk)
