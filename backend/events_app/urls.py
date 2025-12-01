from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list_page, name="event_list"),
    path("events/", views.events_api, name="events_api"),
]
