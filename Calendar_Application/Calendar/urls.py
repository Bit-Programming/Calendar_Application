from django.urls import path
from . import views

urlpatterns = [
    path("<date>/<view>", views.index, name="index"),
    path('event/ajax/<int:event_id>/', views.event_details_ajax, name='event_details_ajax'),
]
