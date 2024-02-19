
from django.urls import path

from balfolk_music.events.views import (
    FestivalsIndexView, EventDetailFeed, EventFeed, EventAPICreateEditView
)

app_name = "events"
urlpatterns = [
    path('feed.ics', EventFeed(), name="event-feed"),
    path('ical/<int:pk>/feed.ics', EventDetailFeed(), name="single-event-ical"),
    path('create', EventAPICreateEditView.as_view(), name="event-create"),
    path('<int:pk>/', EventAPICreateEditView.as_view(), name="event-edit"),
    path("", view=FestivalsIndexView.as_view(), name="festival-list"),
]
