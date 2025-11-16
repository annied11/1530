from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "date", "category")
    search_fields = ("name", "organization", "location", "category")
