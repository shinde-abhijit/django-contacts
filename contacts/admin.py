from django.contrib import admin
from .models import ContactList


class ContactListAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "contact",
        "email",
        "contact_type",
        "is_favorite",
        "created_at",
        "updated_at",
    )
    list_filter = ("contact_type", "gender", "is_favorite", "created_at")
    search_fields = ("first_name", "last_name", "contact", "email", "company")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(ContactList, ContactListAdmin)
