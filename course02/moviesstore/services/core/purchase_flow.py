from django.db import transaction
from services.domain.wallet_service import WalletService
from services.domain.license_service import LicenseService
from apps.orders.models import PurchaseOrder, PurchaseOrderItem


class PurchaseFlow:

    @staticmethod
    @transaction.atomic
    def purchase_movie(user, movie):
        order = PurchaseOrder.objects.create(
            user=user,
            total_coin=movie.price_coin,
        )

        item = PurchaseOrderItem.objects.create(
            order=order,
            movie=movie,
            price_coin=movie.price_coin,
        )

        WalletService.debit(
            user=user,
            amount=movie.price_coin,
            tx_type="PURCHASE",
            ref_type="ORDER",
            ref_id=order.id,
        )

        LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=item,
        )

        order.status = PurchaseOrder.Status.COMPLETED
        order.save(update_fields=["status"])

        return order