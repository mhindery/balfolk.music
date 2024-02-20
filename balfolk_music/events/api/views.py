from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import CalendarListSerializer
# from .serializers import FestivalListSerializer, CalendarListSerializer, FestivalDetailSerializer, CourseSerializer, BallListSerializer, BallDetailSerializer
from balfolk_music.events.models import Event, Festival, Course, Ball
from rest_framework.response import Response


class CalendarEventViewSet(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return Event.objects.filter(visible=True).only(
                'id',
                'name',
                'starting_datetime',
                'ending_datetime',
                'country',
                'event_type',
            ).order_by(
                '-ending_datetime'
            )
        return Event.objects.filter(visible=True)

    def get_serializer_class(self):
        return CalendarListSerializer
