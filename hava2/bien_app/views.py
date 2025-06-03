from django.shortcuts import render, get_object_or_404, redirect
from .models import Propriete
from .forms import ProprieteForm, ImageUploadForm
from .models import Image

def propriete_detail(request, pk):
    propriete = get_object_or_404(Propriete, pk=pk)
    images = propriete.images.all()
    return render(request, 'bien/detail.html', {
        'propriete': propriete,
        'images': images
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