from rest_framework.response import Response


class ApiResponseMixin:
    """
    统一返回结构：
    - 成功：code=0
    - 失败：按 HTTP status 映射语义 code
    - 如果 response.data 已是统一结构，则跳过
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
            if response.status_code == 400:
                response.data = {"code": 40001, "message": "validation_error", "data": response.data}
            elif response.status_code == 401:
                response.data = {"code": 40101, "message": "unauthorized", "data": response.data}
            elif response.status_code == 403:
                response.data = {"code": 40301, "message": "forbidden", "data": response.data}
            elif response.status_code == 404:
                response.data = {"code": 40401, "message": "not_found", "data": response.data}
            else:
                response.data = {"code": 50002, "message": "request_error", "data": response.data}
            return response

        response.data = {"code": 0, "message": "ok", "data": response.data}
        return response