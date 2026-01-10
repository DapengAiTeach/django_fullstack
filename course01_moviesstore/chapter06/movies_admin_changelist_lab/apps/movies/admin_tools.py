from django.core.paginator import Paginator

class FastCountPaginator(Paginator):
    """
    演示版分页器：
    - 通过缓存 count，减少重复 count
    - 在真实大表中，你可能会用“近似 count / 延迟 count / 条件化 count”
    """
    @property
    def count(self):
        if not hasattr(self, "_cached_count"):
            self._cached_count = super().count  # 仍会 count 一次，但避免重复
        return self._cached_count