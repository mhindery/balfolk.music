from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models.functions import ExtractYear
from django.utils.translation import gettext_lazy as _

from balfolk_music.events.models import Ball, Course, Event, Festival

User = get_user_model()


class EventYearFilter(admin.SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        year_list = Event.objects.annotate(y=ExtractYear("start_timestamp")).order_by("y").values_list("y", flat=True).distinct()
        return [(str(y), _(str(y))) for y in year_list]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(start_timestamp__year=self.value())
        return queryset


class EventAdminMixin:
    list_display = ["name", "starting_datetime", "city", "country", "source", "visible", "has_address_info"]
    list_filter = ["visible", "country"]
    readonly_fields = [
        "created_at",
        "starting_datetime",
        "ending_datetime",
    ]

    @admin.display(description="Has address info", boolean=True)
    def has_address_info(self, obj):
        return all([obj.address, obj.lattitude, obj.longitude])


@admin.register(Festival)
class FestivalAdmin(EventAdminMixin, admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["-starting_datetime"]

    # date_hierarchy = 'start_timestamp'

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Course)
class CourseAdmin(EventAdminMixin, admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["-starting_datetime"]

    # date_hierarchy = 'start_timestamp'


@admin.register(Ball)
class BallAdmin(EventAdminMixin, admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["-starting_datetime"]

    def get_queryset(self, request):
        return super().get_queryset(request)

    # date_hierarchy = 'start_timestamp'
