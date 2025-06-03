from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.auth_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("agent/", views.agent_dashboard, name="agent_dashboard"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("manger/users", views.manage_user, name="manage_users"),
    path('/manager/users/delete/<str:email>/', views.delete_user, name='delete_user'),


]