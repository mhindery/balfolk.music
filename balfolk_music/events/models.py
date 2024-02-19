import arrow
from django.db import models
from django.utils import timezone
import pycountry
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class EventDate(models.Model):
    """EventDate represents a date on which an event can occur."""
    date = models.DateField(unique=True)

    class Meta:
        ordering = ['date', ]

    def __str__(self) -> str:
        return self.date.isoformat()


class Event(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Time information
    # Festival: continuous from start on first date to end on last date
    # Course: from start to end on recurring dates
    # Ball: continuous from start on first date to end on last date
    start_timestamp = models.TimeField()
    end_timestamp = models.TimeField()
    dates = models.ManyToManyField(EventDate)

    # Convenience for sorting in DB
    ending_datetime = models.DateTimeField(null=True)
    starting_datetime = models.DateTimeField(null=True)

    def check_dates(self):
        # Add a date for the day it overflows into in case for an ending time of a ball being e.g. 1:30 on the night
        if len(self.dates.all()) == 1 and self.end < self.start:
            date_obj, _ = EventDate.objects.get_or_create(date=arrow.get(self.dates.first().date).shift(days=1).datetime)
            self.dates.add(date_obj)

    @property
    def start(self):
        dates = [x for x in self.dates.all()]
        if not dates:
            return arrow.get().datetime
        date = dates[0].date
        return arrow.get(date.isoformat() + ' ' + self.start_timestamp.isoformat()).datetime

    @property
    def end(self):
        dates = [x for x in self.dates.all()]
        if not dates:
            return arrow.get().datetime
        date = dates[-1].date
        return arrow.get(date.isoformat() + ' ' + self.end_timestamp.isoformat()).datetime

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    organizer = models.CharField(max_length=128, blank=True)
    site = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    banner_image = models.URLField(blank=True)
    poster_image = models.URLField(blank=True)
    pricing = models.TextField(blank=True)
    schedule = models.TextField(blank=True, help_text='Schedule, with e.g. the bands that are playing')

    @property
    def banner_image_url(self):
        if self.banner_image:
            return self.banner_image
        return 'https://www.creactiviste.fr/storage/2019/10/AsQueerAsFolk-1280x720.png'

    def ical_link(self):
        return settings.SITE_HOST + reverse('events:single-event-ical', kwargs={'pk': self.id})

    # Location todo
    address = models.TextField(blank=True)
    city = models.CharField(max_length=32, blank=True)
    lattitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=3, choices=[(x.alpha_2, x.name) for x in pycountry.countries], blank=True)

    def fill_country(self):
        if self.folkbende_id and not self.country:
            self.country = 'BE'
        if self.balfolknl_id and not self.country:
            self.country = 'NL'
        if self.city and not self.country:
            if self.city in ['Leuven', 'Antwerpen', 'Roeselare', 'Waregem', 'Heverlee', 'Watermaal-Bosvoorde', 'Grandmenil', 'Zingem', 'Gooik', 'Aalst', 'Namur', 'Namen', 'Charleroi', 'Uccle', 'Limburg', 'Kortrijk', 'Mechelen', 'Wijgmaal', 'Diest', 'Elsene', 'Belsele', 'Asse', 'Lebbeke', 'Brussels']:
                self.country = 'BE'
                return

    def correct_country_to_alpha_2(self):
        if self.country.lower() == 'turkey':
            self.country = 'TR'
            return

        matches = pycountry.countries.search_fuzzy(self.country)
        if matches:
            self.country = matches[0].alpha_2

    class Type(models.TextChoices):
        FESTIVAL = "festival", _("Festival")
        COURSE = "course", _("Course")
        BALL = "ball", _("Ball")

    event_type = models.CharField(max_length=16, choices=Type.choices, default=Type.FESTIVAL)

    class Meta:
        indexes = [
            models.Index(fields=["event_type", "visible"]),
            models.Index(fields=["visible", "event_type"]),
        ]

    def get_balfolk_music_url(self) -> str:
        if self.event_type == self.Type.FESTIVAL:
            return f'{settings.SITE_HOST}/festivals/{self.id}'
        if self.event_type == self.Type.BALL:
            return f'{settings.SITE_HOST}/balls/{self.id}'
        if self.event_type == self.Type.COURSE:
            return f'{settings.SITE_HOST}/courses/{self.id}'

        return settings.SITE_HOST

    visible = models.BooleanField(default=True)

    class Source(models.TextChoices):
        FOLKBALBENDE = 'folkbalbende', 'FolkBalBende'
        BALFOLK_NL = 'balfolk.nl', 'Balfolk.nl'
        FOLKDANCE_PAGE = 'folkdance.page', 'Folkdance.page'
        WEBSITE = 'website', 'website'

    source = models.CharField(max_length=24, choices=Source.choices)
    folkbende_id = models.IntegerField(blank=True, null=True)
    balfolknl_id = models.CharField(max_length=512, blank=True, null=True)
    folkdancepage_id = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.get_event_type_display()}: {self.name}'

    def fill_geo_info(self):
        import requests
        import pycountry
        import urllib.parse
        if self.longitude and self.lattitude:
            try:
                data = requests.get(
                    url='http://api.geonames.org/addressJSON?lat={lat}&lng={lng}&username=mhindery'.format(
                        lat=self.lattitude,
                        lng=self.longitude,
                    ),
                    timeout=(2, 10),
                ).json()
            except Exception as e:
                print(e)
                return
            if 'address' in data:
                address = data['address']
                country = pycountry.countries.get(alpha_2=address['countryCode'])
                self.country = country.alpha_3
                self.city = address['locality']
                self.address = f'{address["street"]} {address["houseNumber"]}, {
                    address["postalcode"]} {address["locality"]}'
        if self.address:
            try:
                data = requests.get(
                    url='http://api.geonames.org/geoCodeAddressJSON?q={q}&username=mhindery'.format(
                        q=urllib.parse.quote(self.address),
                    ),
                    timeout=(2, 10),
                ).json()
            except Exception as e:
                print(e)
                return
            if 'address' in data:
                address = data['address']
                self.country = address['countryCode']
                self.lattitude = address['lat']
                self.longitude = address['lng']
                self.city = address['locality']
        if self.address and not self.city:
            self.city = self.address.split(' ')[-1]

    def save(self, *args, **kwargs):
        # if not all([self.lattitude, self.longitude, self.address, self.city, self.country]):
        #     self.fill_geo_info()
        #     if not self.country:
        #         self.country = 'BEL'
        if self.id:
            self.ending_datetime = self.end
            self.starting_datetime = self.start
            self.check_dates()
        self.fill_country()
        if self.country and len(self.country) > 2:
            self.correct_country_to_alpha_2()
        return super().save(*args, **kwargs)


class FestivalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(event_type=Event.Type.FESTIVAL)


class Festival(Event):
    objects = FestivalManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.event_type = self.Type.FESTIVAL


class CourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(event_type=Event.Type.COURSE)


class Course(Event):
    objects = CourseManager()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.event_type = self.Type.COURSE

    class Meta:
        proxy = True


class BallManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(event_type=Event.Type.BALL)


class Ball(Event):
    objects = BallManager()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.event_type = self.Type.BALL

    class Meta:
        proxy = True
