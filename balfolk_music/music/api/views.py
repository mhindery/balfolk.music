from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from balfolk_music.music.models import Playlist, Song

from .serializers import PlaylistSerializer, SongSerializer


class PlaylistViewSet(ListModelMixin, GenericViewSet):
    serializer_class = PlaylistSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Playlist.objects.filter(visible=True)


class SongViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = SongSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Song.objects.filter(visible=True)
