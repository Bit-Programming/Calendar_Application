from django.urls import path
from . import views

urlpatterns = [
    path("<date>/<view>", views.index, name="index"),
    path('event/ajax/<int:event_id>/', views.event_details_ajax, name='event_details_ajax'),
    path('event/ajax/date/<date>/', views.events_for_date, name='events_for_date'),
    path('event/add/', views.add_event, name='add_event'),
    path("Calendar/event/delete/<int:event_id>/", views.delete_event, name="delete_event"),
]
