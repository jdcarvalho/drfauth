from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class TokenAPIMixin(object):
    """
    This mixin will deals the token expiration behavior
    """

    def _is_token_expired(self, token):
        """
        Check if the current token is expired
        """
        from datetime import timedelta
        left_time = self._expires_in(token)
        return left_time < timedelta(seconds=0)

    def _handle_expiration(self, token):
        """
        Deals with expiration
        :param token:
        :return:
        """
        from rest_framework.authtoken.models import Token
        is_expired = self._is_token_expired(token)
        user_id = token.user_id
        if is_expired:
            Token.objects.filter(key=token.key).delete()
            try:
                token = Token.objects.create(user_id=user_id)
            except:
                token = Token.objects.get(user_id=user_id)
        return is_expired, token

    def _expires_in(self, token):
        """
        Show exactly when the token expires
        :param token:
        :return:
        """
        from django.utils import timezone
        from datetime import timedelta
        from drf_cauth.settings import API_TOKEN_SECONDS_EXPIRATION

        time_elapsed = timezone.now() - token.created
        left_time = timedelta(
            seconds=API_TOKEN_SECONDS_EXPIRATION) - time_elapsed
        return left_time


class ExpiringTokenAuthentication(TokenAuthentication, TokenAPIMixin):
    """
    This class deals with token expiration
    """

    def authenticate_credentials(self, key):
        """
        This method handle token and credentials
        :param key:
        :return:
        """
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("The user is not active")

        is_expired, token = self._handle_expiration(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        return token.user, token
