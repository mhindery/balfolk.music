from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import FestivalListSerializer, FestivalDetailSerializer, CourseSerializer, BallListSerializer, BallDetailSerializer
from balfolk_music.events.models import Festival, Course, Ball
from rest_framework.response import Response


class FestivalViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    lookup_field = 'pk'

    def get_queryset(self):
        if self.action == 'list':
            return Festival.objects.filter(visible=True).only(
                'id',
                'name',
                'start_timestamp',
                'end_timestamp',
                'banner_image',
                'city', 'country',
            ).prefetch_related('dates')
        return Festival.objects.filter(visible=True).prefetch_related('dates')

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
                'start_timestamp',
                'end_timestamp',
                'banner_image',
                'city', 'country',
            ).prefetch_related('dates')
        return Ball.objects.filter(visible=True).prefetch_related('dates')

    def get_serializer_class(self):
        if self.action == 'list':
            return BallListSerializer
        return BallDetailSerializer
