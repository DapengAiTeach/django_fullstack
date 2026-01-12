from django.db import transaction


class BaseService:
    """
    所有 Service 的基础类
    """

    @classmethod
    def atomic(cls):
        return transaction.atomic()