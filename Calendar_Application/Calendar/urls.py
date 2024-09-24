from django.urls import path

from . import views

urlpatterns = [
    path("<date_begin>/<date_end>/", views.index, name="index"),
]