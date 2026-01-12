from django.db import transaction
from django.utils import timezone

from apps.wallet.models import Wallet, CoinTransaction
from services.common.exceptions import BalanceNotEnough, NotFound


class WalletService:

    @staticmethod
    def get_or_create(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    @staticmethod
    @transaction.atomic
    def credit(user, amount, tx_type, ref_type, ref_id, operator=None, remark=None):
        wallet = Wallet.objects.select_for_update().filter(user=user).first()
        if not wallet:
            raise NotFound("钱包不存在")
        wallet.balance += amount
        wallet.updated_at = timezone.now()
        wallet.save(update_fields=["balance", "updated_at"])

        CoinTransaction.objects.create(
            user=user,
            operator=operator,
            change_amount=amount,
            balance_after=wallet.balance,
            type=tx_type,
            ref_type=ref_type,
            ref_id=ref_id,
            remark=remark,
        )

    @staticmethod
    @transaction.atomic
    def debit(user, amount, tx_type, ref_type, ref_id, operator=None, remark=None):
        wallet = Wallet.objects.select_for_update().filter(user=user).first()
        if wallet.balance < amount:
            raise BalanceNotEnough("余额不足")
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])
        CoinTransaction.objects.create(
            user=user,
            operator=operator,
            change_amount=-amount,
            balance_after=wallet.balance,
            type=tx_type,
            ref_type=ref_type,
            ref_id=ref_id,
            remark=remark,
        )