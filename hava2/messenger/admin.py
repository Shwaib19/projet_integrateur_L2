from django.contrib import admin
from .models import Discussion, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('contenu', 'date_envoi', 'expediteur', 'destinataire')
    can_delete = False

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_agent', 'id_client', 'date_debut')
    list_filter = ('date_debut', 'id_agent', 'id_client')
    search_fields = ('id_agent__user__first_name', 'id_agent__user__last_name',
                     'id_client__user__first_name', 'id_client__user__last_name')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'discussion', 'expediteur', 'destinataire', 'date_envoi', 'contenu_court')
    list_filter = ('date_envoi',)
    search_fields = ('contenu', 'expediteur__first_name', 'destinataire__first_name')

    def contenu_court(self, obj):
        return (obj.contenu[:50] + '...') if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = 'Contenu'
