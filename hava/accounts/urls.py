from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/",views.register_client, name="register_client"),
    path("register/agent",views.register_agent, name="register_agent"),
    path("register/bailleur",views.register_bailleur, name="register_bailleur"),
    
    
]