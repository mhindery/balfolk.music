
from rest_framework import serializers

from balfolk_music.music.models import Playlist, Song


class PlaylistSerializer(serializers.ModelSerializer[Playlist]):
    class Meta:
        model = Playlist
        fields = [
            'id',
            'name',
            'description',
            'link',
            'platform',
        ]


class SongSerializer(serializers.ModelSerializer[Song]):
    class Meta:
        model = Song
        fields = [
            'id',
            'name',
            'band',
        ]
