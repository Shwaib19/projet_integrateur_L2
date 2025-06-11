from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.propriete_detail, name='propriete_detail'),
    path('ajouter/', views.ajouter_propriete, name='ajouter_propriete'),
    path('favoris/toggle/<int:propriete_id>/', views.toggle_favori, name='toggle_favori'),
    path('favoris/', views.liste_favoris, name='mes_favoris'),
]
