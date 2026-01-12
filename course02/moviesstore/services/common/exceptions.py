class ServiceError(Exception):
    pass


class NotFound(ServiceError):
    pass


class PermissionDenied(ServiceError):
    pass


class BalanceNotEnough(ServiceError):
    pass


class BusinessRuleViolation(ServiceError):
    pass