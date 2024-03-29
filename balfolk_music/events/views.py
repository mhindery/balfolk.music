import arrow
import pycountry
from django.conf import settings
from django_filters import MultipleChoiceFilter
from django_filters import rest_framework as filters
from django_ical.views import ICalFeed
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api.serializers import CalendarListSerializer, EventDetailSerializer, EventListSerializer
from .models import Event, EventDate


class EventFilter(filters.FilterSet):
    # event_type = MultipleCharFilter(field_name="event_type", lookup_expr="contains")
    event_type = MultipleChoiceFilter(choices=Event.Type.choices)
    country = MultipleChoiceFilter(choices=[(x.alpha_2, x.name) for x in pycountry.countries])

    class Meta:
        model = Event
        fields = ["event_type", "country"]


class EventListView(generics.ListAPIView):
    queryset = (
        Event.objects.filter(visible=True)
        .only(
            "id",
            "name",
            "starting_datetime",
            "ending_datetime",
            "banner_image",
            "city",
            "country",
            "event_type",
        )
        .order_by("starting_datetime")
    )
    serializer_class = EventListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter


class CalendarEventListView(generics.ListAPIView):
    queryset = Event.objects.filter(visible=True).only(
        "id",
        "name",
        "starting_datetime",
        "ending_datetime",
        "country",
        "event_type",
    )
    serializer_class = CalendarListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter


class EventAPICreateEditView(APIView):
    permission_classes = []

    def post(self, request, pk=None, *args, **kwargs):
        """
        Create or update the Event with given data
        """
        input_data = dict(request.data)

        # Preprocess the input data to create the dates
        date_pks = []
        for d in input_data.get("dates"):
            obj, _ = EventDate.objects.get_or_create(date=arrow.get(d).date())
            date_pks.append(obj.pk)
        input_data["dates"] = date_pks

        # Update existing instance if requested
        instance = None
        if pk:
            instance = Event.objects.get(pk=pk, visible=True)

        serializer = EventDetailSerializer(instance=instance, data=input_data)
        if serializer.is_valid():
            obj = serializer.save()
            if pk:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        obj = Event.objects.filter(pk=pk, visible=True).first()
        serializer = EventDetailSerializer(obj)
        data = serializer.data
        data["dates"] = [arrow.get(d.date).date().isoformat() for d in EventDate.objects.filter(id__in=data["dates"])]
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        return self.post(request, pk=pk, *args, **kwargs)


class EventFeed(ICalFeed):
    """
    A simple event calender
    """

    product_id = "-//balfolk.music//"
    timezone = "UTC"

    def file_name(self):
        return "balfolk_music_events.ics"

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self):
        if event_types := self.request.GET.get("event_type"):
            return Event.objects.filter(visible=True, event_type__in=event_types.split(","))
        return Event.objects.filter(visible=True)

    def item_location(self, item: Event) -> str:
        return item.address

    def item_geolocation(self, item: Event) -> str:
        if item.longitude:
            return (item.lattitude, item.longitude)
        return None

    def item_guid(self, item: Event) -> str:
        return f"balfolk_event_{item.id}"

    def item_title(self, item: Event):
        return item.name

    def item_description(self, item: Event):
        return item.description

    def item_start_datetime(self, item: Event):
        return item.starting_datetime

    def item_end_datetime(self, item: Event):
        return item.ending_datetime

    def item_link(self, item: Event) -> str:
        if item.event_type == Event.Type.BALL:
            return f"{settings.SITE_HOST}/balls/{item.id}"
        if item.event_type == Event.Type.COURSE:
            return f"{settings.SITE_HOST}/course/{item.id}"
        if item.event_type == Event.Type.FESTIVAL:
            return f"{settings.SITE_HOST}/festival/{item.id}"


class EventDetailFeed(EventFeed):
    """
    Generate Ical with single event in it
    """

    product_id = "-//balfolk.music//"
    timezone = "UTC"

    def file_name(self):
        return f"balfolk_music_events_{self.obj.id}.ics"

    def items(self):
        pk = self.request.resolver_match.kwargs["pk"]
        self.obj = Event.objects.filter(id=pk, visible=True).first()
        if not self.obj:
            raise Exception("unknown object")
        return [self.obj]
