from rest_framework.response import Response


class ApiResponseMixin:
    """
    统一返回结构：
    - finalize_response 包装 response.data
    - 若 response.data 已是统一结构（全局异常 handler 已包装），则跳过
    """

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if not isinstance(response, Response):
            return response

        if response.status_code == 204:
            return response

        if isinstance(response.data, dict) and {"code", "message", "data"}.issubset(response.data.keys()):
            return response

        if response.status_code >= 400:
            # 理论上这里不会频繁命中，因为异常交给全局 handler
            response.data = {"code": 50002, "message": "request_error", "data": response.data}
        else:
            response.data = {"code": 0, "message": "ok", "data": response.data}

        return response