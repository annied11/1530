from django.contrib import admin
from .models import Event, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "date", "category")
    search_fields = ("name", "organization__name", "location", "category")
    list_filter = ("organization", "category", "date")
