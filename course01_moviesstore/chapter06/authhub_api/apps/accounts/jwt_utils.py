import time
import os
import jwt
from django.conf import settings

from apps.common.exceptions import InvalidOrExpiredToken


def _now() -> int:
    return int(time.time())


def build_access_token(user_id: int, username: str) -> str:
    """
    Access Token：
    - 短有效期
    - 携带最小必要信息（user_id/username）
    """
    ttl = int(os.getenv("JWT_ACCESS_TTL_SECONDS", "300"))
    payload = {
        "type": "access",
        "sub": str(user_id),
        "username": username,
        "iat": _now(),
        "exp": _now() + ttl,
    }
    key = os.getenv("JWT_SIGNING_KEY", settings.SECRET_KEY)
    return jwt.encode(payload, key, algorithm="HS256")


def build_refresh_token(user_id: int, username: str) -> str:
    """
    Refresh Token：
    - 长有效期
    - 用于换取新 access
    """
    ttl = int(os.getenv("JWT_REFRESH_TTL_SECONDS", "604800"))
    payload = {
        "type": "refresh",
        "sub": str(user_id),
        "username": username,
        "iat": _now(),
        "exp": _now() + ttl,
    }
    key = os.getenv("JWT_SIGNING_KEY", settings.SECRET_KEY)
    return jwt.encode(payload, key, algorithm="HS256")


def decode_token(token: str) -> dict:
    """
    解码并校验 exp
    """
    key = os.getenv("JWT_SIGNING_KEY", settings.SECRET_KEY)
    try:
        return jwt.decode(token, key, algorithms=["HS256"])
    except jwt.PyJWTError as e:
        raise InvalidOrExpiredToken(detail=str(e))


def refresh_access_token(refresh_token: str) -> str:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise InvalidOrExpiredToken(detail="token type is not refresh")

    user_id = int(payload["sub"])
    username = payload.get("username", "")
    return build_access_token(user_id=user_id, username=username)