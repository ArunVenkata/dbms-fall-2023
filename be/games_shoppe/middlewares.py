import os
import pickle

from django.conf import settings
from typing import Callable
from userauth.models import User
from oauth2_provider.models import AccessToken



class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization", "")
        access_token = token[-1] if (token := token.split()) else ""
        request.auth_user = None

        if not access_token:
            return self.get_response(request)

        token_instance = AccessToken.objects.filter(token=f"{access_token}").first()

        if not token_instance:
            return self.get_response(request)


        setattr(request, "auth_user", token_instance.user)

        response = self.get_response(request)

        return response