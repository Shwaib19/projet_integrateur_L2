
from django.urls import path
from . import views 

urlpatterns = [
    path('prendre/<int:propriete_id>/', views.prendre_rendez_vous, name='prendre_rendez_vous'),
    path('rendez-vous/', views.mes_rendez_vous, name='mes_rdv'),
    path('annuler/<int:rdv_id>/', views.annuler_rendez_vous, name='annuler_rendez_vous'),
    path('mes-rdv-agent/', views.rendez_vous_agent, name='rdv_agent'),
    path('modifier_rdv/<int:rdv_id>/', views.modif_statut_rdv, name='modif_statut_rdv'),
]