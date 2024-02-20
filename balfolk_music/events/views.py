
import arrow
from django.views.generic import ListView
from django_ical.views import ICalFeed
from .models import Festival, Ball, Course, Event, EventDate
from rest_framework.views import APIView
from .api.serializers import EventSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import serializers, status


class FestivalsIndexView(ListView):
    template_name = 'events/festivals_index.html'
    model = Festival

    def get_queryset(self):
        return self.model.objects.filter(visible=True).order_by('start_timestamp')


class EventAPICreateEditView(APIView):
    permission_classes = []

    def post(self, request, pk=None, *args, **kwargs):
        '''
        Create or update the Event with given data
        '''
        input_data = dict(request.data)
        # input_data['visible'] = False

        # Preprocess the input data to create the dates
        date_pks = []
        for d in input_data.get('dates'):
            obj, _ = EventDate.objects.get_or_create(date=arrow.get(d).date())
            date_pks.append(obj.pk)
        input_data['dates'] = date_pks

        # Update existing instance if requested
        instance = None
        if pk:
            instance = Event.objects.get(pk=pk)

        serializer = EventSerializer(instance=instance, data=input_data)
        if serializer.is_valid():
            obj = serializer.save()
            # print(f'Created {obj}')
            if pk:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        obj = Event.objects.filter(pk=pk).first()
        serializer = EventSerializer(obj)
        data = serializer.data
        data['dates'] = [arrow.get(d.date).date().isoformat() for d in EventDate.objects.filter(id__in=data['dates'])]
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        return self.post(request, pk=pk, *args, **kwargs)


class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//balfolk.music//'
    timezone = 'UTC'

    def file_name(self):
        return "balfolk_music_events.ics"

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self):
        if event_types := self.request.GET.get('event_type'):
            return Event.objects.filter(event_type__in=event_types).order_by('id').prefetch_related('dates')
        return Event.objects.all().order_by('id').prefetch_related('dates')

    def item_location(self, item: Event) -> str:
        return item.address

    def item_geolocation(self, item: Event) -> str:
        return (item.lattitude, item.longitude)

    def item_guid(self, item: Event) -> str:
        return f'balfolk_event_{item.id}'

    def item_title(self, item: Event):
        return item.name

    def item_description(self, item: Event):
        return item.description

    def item_start_datetime(self, item: Event):
        return item.start

    def item_end_datetime(self, item: Event):
        return item.end

    def item_link(self, item: Event) -> str:
        if item.event_type == Event.Type.BALL:
            return f'{settings.SITE_HOST}/balls/{item.id}'
        if item.event_type == Event.Type.COURSE:
            return f'{settings.SITE_HOST}/course/{item.id}'
        if item.event_type == Event.Type.FESTIVAL:
            return f'{settings.SITE_HOST}/festival/{item.id}'


class EventDetailFeed(EventFeed):
    """
    Generate Ical with single event in it
    """
    product_id = '-//balfolk.music//'
    timezone = 'UTC'

    def file_name(self):
        return f"balfolk_music_events_{self.obj.id}.ics"

    def items(self):
        pk = self.request.resolver_match.kwargs['pk']
        self.obj = Event.objects.filter(id=pk).prefetch_related('dates').first()
        if not self.obj:
            raise Exception('unknown object')
        return [self.obj]
