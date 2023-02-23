from django.contrib import admin
from .models import events
# Register your models here.
@admin.register(events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['jour','periode','horaires','nom']
    ordering = ('jour','periode','horaires','nom')