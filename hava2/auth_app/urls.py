from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.auth_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("agent/", views.agent_dashboard, name="agent_dashboard"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("manager/users", views.manage_user, name="manage_users"),
    path('manager/users/delete/<str:email>/', views.delete_user, name='delete_user'),
    path("acceuille", views.redirect_user, name="redirect_user"),
    path("manager/users/add", views.manager_add_user, name="manager_add_user"),
    path("manager/agents", views.liste_agents,name="liste_agent"),
    path('manager/clients/<int:agent_id>/', views.clients_par_agent, name='clients_par_agent'),
    path('manager/clients/retirer/<int:client_id>/', views.retirer_client, name='retirer_client'),
    path('modifier/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('mes_proprietes/', views.proprietes_du_bailleur, name='mes_proprietes'),
]