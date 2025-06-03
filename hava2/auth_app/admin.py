from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AgentProfile, ClientProfile

# Personnalisation de l'affichage des utilisateurs
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password','first_name','last_name')}),
        ('Personal info', {'fields': ('email', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

# Enregistrement des modèles
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AgentProfile)
admin.site.register(ClientProfile)
