from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.common.mixins import ApiResponseMixin
from apps.common.exceptions import InvalidCredentials
from apps.accounts.serializers import LoginSerializer, JwtRefreshSerializer
from apps.accounts.jwt_utils import build_access_token, build_refresh_token, refresh_access_token

User = get_user_model()


class SessionLoginView(ApiResponseMixin, APIView):
    authentication_classes = ()  # 登录不需要认证
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
        if not user:
            raise InvalidCredentials()

        login(request, user)
        return Response({"username": user.username})


class SessionLogoutView(ApiResponseMixin, APIView):
    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


class TokenLoginView(ApiResponseMixin, APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
        if not user:
            raise InvalidCredentials()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class JwtLoginView(ApiResponseMixin, APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
        if not user:
            raise InvalidCredentials()

        access = build_access_token(user_id=user.id, username=user.username)
        refresh = build_refresh_token(user_id=user.id, username=user.username)

        return Response({"access": access, "refresh": refresh}, status=status.HTTP_200_OK)


class JwtRefreshView(ApiResponseMixin, APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = JwtRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = refresh_access_token(serializer.validated_data["refresh"])
        return Response({"access": access}, status=status.HTTP_200_OK)