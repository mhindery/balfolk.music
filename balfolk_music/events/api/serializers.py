
from rest_framework import serializers

from balfolk_music.events.models import Festival, Course, Ball, Event


class EventSerializer(serializers.ModelSerializer[Event]):
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
            'visible',
            'balfolk_music_url',
        ]


class FestivalListSerializer(serializers.ModelSerializer[Festival]):
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    class Meta:
        model = Festival
        fields = [
            'id',
            'start',
            'end',
            'name',
            'banner_image_url',
            'country_name',
            'city',
        ]


class FestivalDetailSerializer(serializers.ModelSerializer[Festival]):
    country_code = serializers.CharField(source='country', read_only=True)
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    ical_link = serializers.CharField(read_only=True)

    class Meta:
        model = Festival
        fields = [
            'id',
            'start',
            'end',
            'name',
            'ical_link',
            'description',
            'banner_image_url',
            'poster_image',
            'organizer',
            'site',
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
        ]


class CourseSerializer(serializers.ModelSerializer[Course]):
    country_code = serializers.CharField(source='country', read_only=True)
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    dates = serializers.StringRelatedField(many=True)
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    ical_link = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'start',
            'end',
            'dates',
            'name',
            'description',
            'banner_image_url',
            'poster_image',
            'organizer',
            'site',
            'facebook',
            'address',
            'lattitude',
            'ical_link',
            'longitude',
            'country_code',
            'country_name',
            'schedule',
            'pricing',
            'city',
            'event_type',
            'event_type_display',
        ]


class BallListSerializer(serializers.ModelSerializer[Ball]):
    country_name = serializers.CharField(source='get_country_display', read_only=True)
    country_code = serializers.CharField(source='country', read_only=True)

    class Meta:
        model = Ball
        fields = [
            'id',
            'start',
            'end',
            'name',
            'country_code',
            'country_name',
            'city',
        ]


class BallDetailSerializer(serializers.ModelSerializer[Ball]):
    country_code = serializers.CharField(source='country', read_only=True)
    country_name = serializers.CharField(source='get_country_display', read_only=True)

    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    ical_link = serializers.CharField(read_only=True)

    class Meta:
        model = Ball
        fields = [
            'id',
            'start',
            'end',
            'name',
            'description',
            'banner_image_url',
            'poster_image',
            'organizer',
            'ical_link',
            'site',
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
        ]
