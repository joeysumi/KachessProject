from django.contrib import admin
from .models import Trip, TripInvolvement


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "start_date", "end_date")
    list_filter = ("organization",)
    search_fields = ("name", "location")


@admin.register(TripInvolvement)
class TripInvolvementAdmin(admin.ModelAdmin):
    list_display = ("trip", "person", "status")
    list_filter = ("status",)
    search_fields = (
        "person__first_name",
        "person__last_name",
        "person__email",
        "trip__name",
    )
