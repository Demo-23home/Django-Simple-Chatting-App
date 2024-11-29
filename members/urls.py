from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.user_signup, name="signup"),
    path("login", views.user_login, name="login"),
    path("logout", views.logout, name="logout"),
    path("", views.home, name="home"),
]
