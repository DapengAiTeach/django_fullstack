from rest_framework.exceptions import APIException


class BusinessException(APIException):
    status_code = 400
    default_code = "business_error"
    default_detail = "business error"
    business_code = 40900

    def __init__(self, detail=None, code=None, business_code=None):
        super().__init__(detail=detail, code=code)
        if business_code is not None:
            self.business_code = business_code


class InvalidCredentials(BusinessException):
    default_code = "invalid_credentials"
    default_detail = "用户名或密码错误"
    business_code = 40111


class InvalidOrExpiredToken(BusinessException):
    default_code = "invalid_or_expired_token"
    default_detail = "token 无效或已过期"
    business_code = 40112