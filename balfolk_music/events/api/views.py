from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import FestivalListSerializer, CalendarListSerializer, FestivalDetailSerializer, CourseSerializer, BallListSerializer, BallDetailSerializer
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
            # ).order_by('id')[:100]
        return Event.objects.filter(visible=True)

    def get_serializer_class(self):
        return CalendarListSerializer


class FestivalViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    lookup_field = 'pk'

    def get_queryset(self):
        if self.action == 'list':
            return Festival.objects.filter(visible=True).only(
                'id',
                'name',
                'starting_datetime',
                'ending_datetime',
                'banner_image',
                'city', 'country',
            )
        return Festival.objects.filter(visible=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return FestivalListSerializer
        return FestivalDetailSerializer


class CourseViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Course.objects.filter(visible=True).prefetch_related('dates')


class BallViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    lookup_field = 'pk'

    def get_queryset(self):
        if self.action == 'list':
            return Ball.objects.filter(visible=True).only(
                'id',
                'name',
                'starting_datetime',
                'ending_datetime',
                'city', 'country',
            )
            # ).order_by('id')[:100]
        return Ball.objects.filter(visible=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return BallListSerializer
        return BallDetailSerializer
