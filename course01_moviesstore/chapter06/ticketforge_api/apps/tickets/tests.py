from rest_framework.test import APITestCase
from rest_framework import status
from apps.tickets.models import Ticket


class TicketValidationAndExceptionTests(APITestCase):
    """
    覆盖：
    - 字段级校验（priority/title）
    - 对象级校验（status 联动）
    - 业务异常（状态回退/删除关闭工单）
    - 全局异常结构（code/message/data）
    """

    def test_field_level_validation_should_work(self):
        payload = {"title": "短", "priority": 9, "status": "OPEN"}
        resp = self.client.post("/api/tickets/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data["code"], 40001)
        self.assertEqual(resp.data["message"], "validation_error")
        self.assertIn("title", resp.data["data"])
        self.assertIn("priority", resp.data["data"])

    def test_object_level_validation_should_work(self):
        payload = {
            "title": "关闭工单但无邮箱",
            "description": "描述至少 10 字以上……",
            "priority": 3,
            "status": "CLOSED",
        }
        resp = self.client.post("/api/tickets/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data["code"], 40001)
        self.assertIn("assignee_email", resp.data["data"])

    def test_business_exception_status_rollback_should_work(self):
        # 创建一个 CLOSED 工单
        ticket = Ticket.objects.create(
            title="已关闭工单",
            description="已关闭",
            priority=2,
            status=Ticket.Status.CLOSED,
            assignee_email="ops@example.com",
        )

        # 尝试回退到 OPEN，应该触发业务异常
        resp = self.client.patch(
            f"/api/tickets/{ticket.id}/",
            data={"status": "OPEN"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data["code"], 40901)
        self.assertEqual(resp.data["message"], "ticket_status_rollback_not_allowed")

    def test_business_exception_delete_closed_ticket_should_work(self):
        ticket = Ticket.objects.create(
            title="不可删除关闭工单",
            description="已关闭",
            priority=2,
            status=Ticket.Status.CLOSED,
            assignee_email="ops@example.com",
        )

        resp = self.client.delete(f"/api/tickets/{ticket.id}/")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data["code"], 40902)
        self.assertEqual(resp.data["message"], "delete_closed_ticket_not_allowed")