from django.urls import path
from . import views



urlpatterns = [
path("discussion_agent/", views.liste_discussions_agent, name="liste_discussions_agent"),
path("discussion_client/", views.discussions_client, name="discussions_client"),
# urls.py
path('messages-discussion/<int:discussion_id>/', views.messages_discussion_json, name='messages_discussion_json'),
path('messages-discussion_client/<int:discussion_id>/', views.messages_discussion_json_client, name='messages_discussion_json_client'),

path('envoyer-message/<int:discussion_id>/', views.envoyer_message, name='envoyer_message'),

]