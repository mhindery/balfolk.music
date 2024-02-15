
from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .models import Playlist, Song


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["name", "platform", "visible"]
    list_filter = ['platform', ]
    search_fields = ["name"]

    # date_hierarchy = 'start_timestamp'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'band', 'dance']
    list_filter = ['dance', ]
    search_fields = ['name', 'band', 'dance']
