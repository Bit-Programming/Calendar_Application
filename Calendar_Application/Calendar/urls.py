from django.urls import path

from . import views

urlpatterns = [
    path("<date>/<view>", views.index, name="index"),
]