from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.mixins import ApiResponseMixin


class ProfileView(ApiResponseMixin, APIView):
    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "is_authenticated": user.is_authenticated,
            }
        )