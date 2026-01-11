from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model

from apps.accounts.jwt_utils import decode_token
from apps.common.exceptions import InvalidOrExpiredToken

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Authorization: Bearer <access_token>
    """

    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2:
            return None

        if parts[0] != self.keyword:
            return None

        token = parts[1]
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise InvalidOrExpiredToken(detail="token type is not access")

        user_id = int(payload["sub"])
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise InvalidOrExpiredToken(detail="user not found")

        return (user, token)