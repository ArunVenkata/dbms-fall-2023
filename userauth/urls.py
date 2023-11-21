from django.urls import path
from userauth.models import *
from userauth.views.login import UserLogin
from userauth.views.signup import UserSignUp



urlpatterns = [
    path("login/", UserLogin.as_view(), name="userlogin"),
    path("signup/", UserSignUp.as_view(), name="usersignup")
]