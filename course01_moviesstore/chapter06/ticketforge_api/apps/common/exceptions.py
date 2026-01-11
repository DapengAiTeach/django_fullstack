from rest_framework.exceptions import APIException


class BusinessException(APIException):
    """
    业务异常基类：
    - 子类可通过 business_code 定义业务错误码
    - 若实例化时显式传 business_code，则覆盖子类默认值
    """

    status_code = 400
    default_code = "business_error"
    default_detail = "business error"

    # 子类可覆盖该默认业务码
    business_code = 40900

    def __init__(self, detail=None, code=None, business_code=None):
        super().__init__(detail=detail, code=code)

        # 关键修复点：
        # 不传 business_code 时，保留子类 business_code（避免被 None 覆盖）
        if business_code is not None:
            self.business_code = business_code


class TicketStatusRollbackNotAllowed(BusinessException):
    default_code = "ticket_status_rollback_not_allowed"
    default_detail = "不允许从 CLOSED 回退到 OPEN"
    business_code = 40901


class DeleteClosedTicketNotAllowed(BusinessException):
    default_code = "delete_closed_ticket_not_allowed"
    default_detail = "不允许删除已关闭工单"
    business_code = 40902
