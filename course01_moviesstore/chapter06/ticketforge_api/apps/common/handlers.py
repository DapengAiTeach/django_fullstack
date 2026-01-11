from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied, AuthenticationFailed
from rest_framework.response import Response

from apps.common.exceptions import BusinessException


def api_exception_handler(exc, context):
    """
    全局异常处理：
    - 捕获 DRF 标准异常（ValidationError/NotFound/...）
    - 捕获业务异常（BusinessException）
    - 将其统一成 {code,message,data} 结构

    注意：
    - 这里返回的 Response.data 已经是统一结构
    - ApiResponseMixin 中有重复包装保护，不会二次包装
    """
    response = drf_exception_handler(exc, context)

    # DRF 没处理的异常（比如代码 bug）会返回 None
    if response is None:
        return Response(
            {"code": 50001, "message": "server_error", "data": {"detail": str(exc)}},
            status=500,
        )

    # 默认错误信息：response.data
    data = response.data

    # DRF 标准异常映射
    if isinstance(exc, ValidationError):
        return Response({"code": 40001, "message": "validation_error", "data": data}, status=response.status_code)

    if isinstance(exc, AuthenticationFailed):
        return Response({"code": 40101, "message": "unauthorized", "data": data}, status=response.status_code)

    if isinstance(exc, PermissionDenied):
        return Response({"code": 40301, "message": "forbidden", "data": data}, status=response.status_code)

    if isinstance(exc, NotFound):
        return Response({"code": 40401, "message": "not_found", "data": data}, status=response.status_code)

    # 业务异常映射（允许携带 business_code）
    if isinstance(exc, BusinessException):
        code = getattr(exc, "business_code", 40900)
        return Response(
            {"code": code, "message": exc.default_code, "data": {"detail": response.data}},
            status=response.status_code,
        )

    # 兜底：按 DRF response 状态码处理
    return Response({"code": 50002, "message": "request_error", "data": data}, status=response.status_code)