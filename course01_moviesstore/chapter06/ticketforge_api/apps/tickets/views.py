from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from apps.common.mixins import ApiResponseMixin
from apps.common.exceptions import TicketStatusRollbackNotAllowed, DeleteClosedTicketNotAllowed
from apps.tickets.models import Ticket
from apps.tickets.serializers import TicketSerializer


class TicketViewSet(ApiResponseMixin, ModelViewSet):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer

    def perform_update(self, serializer):
        """
        自定义异常类示例：不允许从 CLOSED 回退到 OPEN
        - 这里使用业务异常（继承 APIException）
        - 抛出后由全局 exception handler 统一输出结构
        """
        instance: Ticket = self.get_object()
        new_status = serializer.validated_data.get("status")

        if instance.status == Ticket.Status.CLOSED and new_status == Ticket.Status.OPEN:
            raise TicketStatusRollbackNotAllowed()

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        删除业务规则：
        - 不允许删除已关闭工单
        """
        instance: Ticket = self.get_object()
        if instance.status == Ticket.Status.CLOSED:
            raise DeleteClosedTicketNotAllowed()

        return super().destroy(request, *args, **kwargs)