from rest_framework.response import Response


class ApiResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if not isinstance(response, Response):
            return response

        if response.status_code == 204:
            return response

        if isinstance(response.data, dict) and {"code", "message", "data"}.issubset(response.data.keys()):
            return response

        if response.status_code >= 400:
            response.data = {"code": 50002, "message": "request_error", "data": response.data}
        else:
            response.data = {"code": 0, "message": "ok", "data": response.data}

        return response