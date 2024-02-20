
from rest_framework import serializers

from balfolk_music.events.models import Festival, Course, Ball, Event


class EventListSerializer(serializers.ModelSerializer[Event]):
    country_code = serializers.CharField(source='country', read_only=True)
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'starting_datetime',
            'ending_datetime',
            'name',
            'banner_image_url',
            'country_code',
            'country_name',
            'city',
        ]


class EventDetailSerializer(serializers.ModelSerializer[Event]):
    country_code = serializers.CharField(source='country', read_only=True)
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    balfolk_music_url = serializers.CharField(source='get_balfolk_music_url', read_only=True)

    ical_link = serializers.CharField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'event_type',
            'start_timestamp',
            'end_timestamp',
            'name',
            'dates',
            'description',
            'banner_image',
            'banner_image_url',
            'poster_image',
            'organizer',
            'site',
            'ical_link',
            'facebook',
            'address',
            'lattitude',
            'longitude',
            'country_code',
            'country_name',
            'schedule',
            'pricing',
            'city',
            'event_type',
            'event_type_display',
            'balfolk_music_url',
            'starting_datetime',
            'ending_datetime',
        ]


class CalendarListSerializer(serializers.ModelSerializer[Event]):
    country_code = serializers.CharField(source='country', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'starting_datetime',
            'ending_datetime',
            'name',
            'country_code',
            'event_type',
        ]
