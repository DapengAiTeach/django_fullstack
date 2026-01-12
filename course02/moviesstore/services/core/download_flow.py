from datetime import timedelta
from django.utils import timezone

from services.domain.license_service import LicenseService
from services.domain.download_service import DownloadService
from services.common.exceptions import PermissionDenied


class DownloadFlow:

    @staticmethod
    def create_download_token(user, movie, device_id):
        if not LicenseService.has_movie_access(user, movie):
            raise PermissionDenied("无下载权限")

        return DownloadService.create_token(
            user=user,
            movie=movie,
            device_id=device_id,
            expires_at=timezone.now() + timedelta(minutes=10),
        )