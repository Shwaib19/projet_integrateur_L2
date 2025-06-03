from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.propriete_detail, name='propriete_detail'),
    path('ajouter/', views.ajouter_propriete, name='ajouter_propriete'),
]
