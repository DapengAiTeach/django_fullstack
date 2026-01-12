from apps.movie_auth.models import UserIdentity
from services.common.exceptions import BusinessRuleViolation


class IdentityService:

    @staticmethod
    def bind_identity(user, identity_type, identifier):
        exists = UserIdentity.objects.filter(
            identity_type=identity_type,
            identifier=identifier
        ).exists()
        if exists:
            raise BusinessRuleViolation("该身份已被占用")
        return UserIdentity.objects.create(
            user=user,
            identity_type=identity_type,
            identifier=identifier,
        )