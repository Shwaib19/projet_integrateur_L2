from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.propriete_detail, name='propriete_detail'),
    path('ajouter/', views.ajouter_propriete, name='ajouter_propriete'),
    path('favoris/toggle/<int:propriete_id>/', views.toggle_favori, name='toggle_favori'),
    path('favoris/', views.liste_favoris, name='mes_favoris'),
    path('proprietes/modifier/<int:pk>/', views.modifier_propriete, name='modifier_propriete'),
    path('proprietes/supprimer-image/<int:image_id>/', views.supprimer_image, name='supprimer_image'),
]
