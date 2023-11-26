from django.urls import path
from userauth.models import *
from userauth.views.login import UserLogin
from userauth.views.signup import UserSignUp
from rest_framework.routers import DefaultRouter

from userauth.views.userlist import UserModelViewSet


router = DefaultRouter()

router.register(r"users", UserModelViewSet, basename="usersview")


urlpatterns = [
    path("login/", UserLogin.as_view(), name="userlogin"),
    path("signup/", UserSignUp.as_view(), name="usersignup")
]

urlpatterns +=router.urls
