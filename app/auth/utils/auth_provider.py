from abc import ABC

from app.auth.services.auth_provider import auth_helper as local_provider


def get_auth_provider(auth_type: str):
    auth_type = auth_type.lower()
    try:
        return __AUTH_PROVIDERS[auth_type]
    except KeyError:
        raise AttributeError(f"{auth_type} is not supported")


class AuthProvider(ABC):
    def validate_token(self, token, **kwargs):
        pass

    def retrieve_token(self, **kwargs):
        pass

    def get_user_info(self, user):
        pass


class LocalAuthProvider(AuthProvider):

    def validate_token(self, token, **kwargs):
        return local_provider.validate_token(token)

    def retrieve_token(self, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        return local_provider.retrieve_token(email, password)

    def get_user_info(self, user):
        return local_provider.get_user_info(user)


__AUTH_PROVIDERS = {
    "local": LocalAuthProvider()
}
