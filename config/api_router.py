from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from balfolk_music.users.api.views import UserViewSet
from balfolk_music.events.api.views import FestivalViewSet, CourseViewSet, BallViewSet, CalendarEventViewSet
from balfolk_music.music.api.views import PlaylistViewSet, SongSerializer, SongViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register('festivals', FestivalViewSet, basename='festival')
router.register('courses', CourseViewSet, basename='course')
router.register('balls', BallViewSet, basename='ball')
router.register('calendar_events', CalendarEventViewSet, basename='calendar_event')
# router.register('playlists', PlaylistViewSet, basename='playlist')
# router.register('songs', SongViewSet, basename='song')


app_name = "api"
urlpatterns = router.urls
