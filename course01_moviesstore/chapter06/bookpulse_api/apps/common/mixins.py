from rest_framework.response import Response


class ApiResponseMixin:
    """
    统一返回结构（企业级 API 契约层）：
    - 通过 finalize_response 改写 response.data
    - 让测试里的 resp.data 与最终输出一致（TDD 友好）
    - 不依赖 Renderer 封装 code/message/data
    """

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        # 只处理 DRF Response
        if not isinstance(response, Response):
            return response

        # 204 No Content：按规范不返回 body
        if response.status_code == 204:
            return response

        # 防止重复包装
        if isinstance(response.data, dict) and {"code", "message", "data"}.issubset(response.data.keys()):
            return response

        status_code = response.status_code

        if status_code >= 400:
            if status_code == 400:
                code = 40001
                message = "validation_error"
            elif status_code == 401:
                code = 40101
                message = "unauthorized"
            elif status_code == 403:
                code = 40301
                message = "forbidden"
            elif status_code == 404:
                code = 40401
                message = "not_found"
            else:
                code = 50001
                message = "request_error"

            response.data = {
                "code": code,
                "message": message,
                "data": response.data,
            }
        else:
            response.data = {
                "code": 0,
                "message": "ok",
                "data": response.data,
            }

        return response