from django.db import models
from django.utils import timezone
import pycountry
from django.utils.translation import gettext_lazy as _


class Playlist(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    description = models.TextField()
    link = models.URLField()

    class Platform(models.TextChoices):
        SPOTIFY = "spotify", _("Spotify")
        SOUNDCLOUD = "soundcloud", _("SoundCloud")
        YOUTUBE = "youtube", _("Youtube")
        APPLE_MUSIC = "apple_music", _("Apple Music")

    platform = models.CharField(max_length=16, choices=Platform.choices)

    visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.get_platform_display()})'


class Song(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    band = models.CharField(max_length=128)

    class Dance(models.TextChoices):
        MAZURKA = "mazurka", _("Mazurka")
        SCOTTISH = "scottish", _("Scottish")
        WALTZ_3 = "waltz_3", _("Waltz in 3")
        WALTZ_5 = "waltz_5", _("Waltz in 5")
        WALTZ_7 = "waltz_7", _("Waltz in 7")
        JIG = "jig", "Jig / Chappeloise"
        CERCLE = "cercle", "Cercle Circassien"

    dance = models.CharField(max_length=16, choices=Dance.choices)

    visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.band} ({self.get_dance_display()})'
