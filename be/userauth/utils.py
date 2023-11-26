import datetime as dt

from django.db import transaction
from django.utils import timezone
from oauth2_provider.models import RefreshToken, Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token

def create_application(user_instance):
    application, _ = Application.objects.get_or_create(
            user=user_instance,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
    return application


def datetime_from_now(**kwargs):
    """
    :return: datetime with addition of kwargs timedelta
    """
    return timezone.now() + dt.timedelta(**kwargs)

def get_access_token(user):
    """
    removes old token attached with user
    create new token and access token for the user
    :param user: account instance
    :return: access-token in json format
    """
    app = Application.objects.first()
    # application does not exist so create
    if not app:
        app = create_application(user)
    with transaction.atomic():
        access_token_instance = AccessToken.objects.create(
            user=user,
            application=app,
            expires=datetime_from_now(
                seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
            ),
            token=generate_token(),
            scope="read write",
        )
        RefreshToken.objects.create(
            user=user,
            application=app,
            token=generate_token(),
            access_token=access_token_instance,
        )
        return get_token_json(access_token_instance)
    


def get_token_json(instance):
    """
    :param instance: access token instance
    :return: json format of access-token, refresh-token with scope and expire time
    """
    token = {
        "access_token": instance.token,
        "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        "refresh_token": instance.refresh_token.token,
        "scope": instance.scope,
    }

    return token