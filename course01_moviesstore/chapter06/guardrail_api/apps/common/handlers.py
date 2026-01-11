from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
)
from rest_framework.response import Response


def api_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {"code": 50001, "message": "server_error", "data": {"detail": str(exc)}},
            status=500,
        )

    data = response.data

    if isinstance(exc, ValidationError):
        return Response({"code": 40001, "message": "validation_error", "data": data}, status=response.status_code)

    # ✅ 未登录（NotAuthenticated）
    # 你的测试期望 code=40301，因此这里按 forbidden 语义返回
    if isinstance(exc, NotAuthenticated):
        return Response({"code": 40301, "message": "forbidden", "data": data}, status=response.status_code)

    if isinstance(exc, AuthenticationFailed):
        return Response({"code": 40101, "message": "unauthorized", "data": data}, status=response.status_code)

    if isinstance(exc, PermissionDenied):
        return Response({"code": 40301, "message": "forbidden", "data": data}, status=response.status_code)

    if isinstance(exc, NotFound):
        return Response({"code": 40401, "message": "not_found", "data": data}, status=response.status_code)

    return Response({"code": 50002, "message": "request_error", "data": data}, status=response.status_code)
