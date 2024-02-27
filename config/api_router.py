from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from balfolk_music.music.api.views import PlaylistViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("playlists", PlaylistViewSet, basename="playlist")


app_name = "api"
urlpatterns = router.urls
