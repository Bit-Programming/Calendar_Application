from django.contrib import admin

# Temporary
from .models import Question

from .models import Event

admin.site.register(Question)
admin.site.register(Event)