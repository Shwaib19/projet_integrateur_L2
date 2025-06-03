from django.contrib import admin

from django.contrib import admin
from .models import Propriete, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProprieteAdmin(admin.ModelAdmin):
    list_display = ('type', 'localisation', 'prix', 'statut', 'option')
    inlines = [ImageInline]

admin.site.register(Propriete, ProprieteAdmin)
