from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tickets.views import TicketViewSet

app_name = "tickets"

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]