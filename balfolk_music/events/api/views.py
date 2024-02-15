from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import FestivalSerializer, CourseSerializer, BallSerializer
from balfolk_music.events.models import Festival, Course, Ball


class FestivalViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FestivalSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Festival.objects.filter(visible=True).prefetch_related('dates')


class CourseViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Course.objects.filter(visible=True).prefetch_related('dates')


class BallViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BallSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Ball.objects.filter(visible=True).prefetch_related('dates')
