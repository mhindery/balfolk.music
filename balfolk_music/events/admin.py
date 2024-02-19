from django.db.models.functions import ExtractYear
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model, decorators

from django.utils.translation import gettext_lazy as _

from balfolk_music.events.models import Festival, Course, Event, Ball

User = get_user_model()


list_display = ["name", "starting_datetime", "city", "country"]


class EventYearFilter(admin.SimpleListFilter):
    title = _('year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        year_list = Event.objects.annotate(
            y=ExtractYear('start_timestamp')
        ).order_by('y').values_list('y', flat=True).distinct()
        return [
            (str(y), _(str(y))) for y in year_list
        ]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(start_timestamp__year=self.value())
        return queryset


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = list_display
    list_filter = ['visible', 'country']
    readonly_fields = ['created_at', ]
    search_fields = ["name"]
    ordering = ['-starting_datetime']

    # date_hierarchy = 'start_timestamp'

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = list_display
    list_filter = ['visible', 'country']
    readonly_fields = ['created_at', ]
    search_fields = ["name"]
    ordering = ['-starting_datetime']

    # date_hierarchy = 'start_timestamp'


@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = list_display
    list_filter = ['visible', 'country']
    readonly_fields = ['created_at', 'starting_datetime', 'ending_datetime']
    search_fields = ["name"]
    ordering = ['-starting_datetime']

    def get_queryset(self, request):
        return super().get_queryset(request)

    # date_hierarchy = 'start_timestamp'
