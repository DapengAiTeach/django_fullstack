from rest_framework.response import Response


class ApiResponseMixin:
    """
    统一包装 DRF 的 Response.data，让测试里的 resp.data 也符合统一结构：

    成功：
    {
      "code": 0,
      "message": "ok",
      "data": <原始数据>
    }

    失败（400）：
    {
      "code": 40001,
      "message": "validation_error",
      "data": <原始错误结构>
    }

    注意：
    - Renderer 只影响最终输出 JSON 的“渲染结果”
    - APITestCase 里的 resp.data 取的是“渲染前的 Response.data”
    - 所以必须在视图层把 Response.data 直接改成统一结构（这才是 TDD 友好）
    """

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        # 只处理 DRF 的 Response
        if not isinstance(response, Response):
            return response

        # 204 No Content：HTTP 规范上不应返回 body，保持空
        if response.status_code == 204:
            return response

        # 防止重复包装（比如你以后某些接口手动返回了统一结构）
        if isinstance(response.data, dict) and {"code", "message", "data"}.issubset(response.data.keys()):
            return response

        status_code = response.status_code

        # 根据状态码区分成功 / 失败
        if status_code >= 400:
            # 400：参数校验错误最常见
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
