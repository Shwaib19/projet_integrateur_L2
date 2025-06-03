from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('email', 'nom', 'prenom', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'mot_de_passe')}),
        ('Infos personnelles', {'fields': ('nom', 'prenom', 'telephone', 'adresse')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mot_de_passe1', 'mot_de_passe2', 'nom', 'prenom', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
