from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'agent',
        'propriete',
        'date_souhaitee',
        'date_confirmee',
        'statut',
    )
    list_filter = ('statut', 'date_souhaitee', 'date_confirmee', 'agent')
    search_fields = ('client__email', 'agent__email', 'propriete__localisation')
    ordering = ('-date_souhaitee',)
    date_hierarchy = 'date_souhaitee'
    readonly_fields = ('client', 'agent', 'propriete')

    fieldsets = (
        (None, {
            'fields': ('client', 'agent', 'propriete', 'statut')
        }),
        ('Dates', {
            'fields': ('date_souhaitee', 'date_confirmee')
        }),
        ('Commentaires', {
            'fields': ('commentaire_client', 'commentaire_agent')
        }),
    )
