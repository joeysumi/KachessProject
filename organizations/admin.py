from django.contrib import admin
from .models import (
    Organization,
    OrganizationMembership,
    Person,
    UserProfile,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role", "created_at")
    list_filter = ("role", "organization")
    search_fields = ("user__username", "organization__name")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("display_name", "preferred_name", "organization", "user", "email")
    list_filter = ("organization",)
    search_fields = ("first_name", "last_name", "preferred_name", "email")

    @admin.display(description="Name")
    def display_name(self, obj):
        return f"{obj.first_name} ({obj.preferred_name}) {obj.last_name}" if obj.preferred_name else f"{obj.first_name} {obj.last_name}"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "email", "phone")
    search_fields = ("first_name", "last_name", "email", "user__username")

    @admin.display(description="Name")
    def display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"