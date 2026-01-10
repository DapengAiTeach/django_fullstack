from django.contrib import admin
from django.db.models import Q

class ScoreLevelFilter(admin.SimpleListFilter):
    title = "评分档位"
    parameter_name = "score_level"

    def lookups(self, request, model_admin):
        return [
            ("top", "高分(>=8.5)"),
            ("mid", "中上(7.5~8.4)"),
            ("low", "一般(<7.5)"),
        ]

    def queryset(self, request, queryset):
        v = self.value()
        if v == "top":
            return queryset.filter(score__gte=8.5)
        if v == "mid":
            return queryset.filter(score__gte=7.5, score__lt=8.5)
        if v == "low":
            return queryset.filter(score__lt=7.5)
        return queryset


class PriceRangeFilter(admin.SimpleListFilter):
    title = "价格区间"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return [
            ("p1", "0~19.9"),
            ("p2", "20~49.9"),
            ("p3", ">=50"),
        ]

    def queryset(self, request, queryset):
        v = self.value()
        if v == "p1":
            return queryset.filter(price__lt=20)
        if v == "p2":
            return queryset.filter(price__gte=20, price__lt=50)
        if v == "p3":
            return queryset.filter(price__gte=50)
        return queryset