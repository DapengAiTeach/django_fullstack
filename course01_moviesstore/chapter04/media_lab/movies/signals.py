# movies/signals.py
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Movie, MoviePhoto


def _delete_file(fieldfile):
    """
    安全删除文件：字段为空或文件不存在都不报错
    """
    if not fieldfile:
        return
    try:
        if fieldfile.path and os.path.exists(fieldfile.path):
            os.remove(fieldfile.path)
    except Exception:
        # 生产环境建议记录日志
        pass


@receiver(post_delete, sender=Movie)
def delete_movie_cover(sender, instance, **kwargs):
    _delete_file(instance.cover)


@receiver(post_delete, sender=MoviePhoto)
def delete_movie_photo(sender, instance, **kwargs):
    _delete_file(instance.image)
