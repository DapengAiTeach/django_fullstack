from django.urls import path
from apps.accounts.views import (
    SessionLoginView,
    SessionLogoutView,
    TokenLoginView,
    JwtLoginView,
    JwtRefreshView,
)

app_name = "accounts"

urlpatterns = [
    path("auth/session/login/", SessionLoginView.as_view(), name="session-login"),
    path("auth/session/logout/", SessionLogoutView.as_view(), name="session-logout"),

    path("auth/token/login/", TokenLoginView.as_view(), name="token-login"),

    path("auth/jwt/login/", JwtLoginView.as_view(), name="jwt-login"),
    path("auth/jwt/refresh/", JwtRefreshView.as_view(), name="jwt-refresh"),
]