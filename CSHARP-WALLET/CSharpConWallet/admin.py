"""This module provides the admin endpoint for the app"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (
    user,
    Contacts,
    FAQs,
    Messages,
    TokenRequests,
    Support,
    HealthRecords,
    Email_verify,
    admin_data
)


class UserAdmin(UserAdmin):
    """This class provides the User endpoint for the app"""

    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_staff",
        "role",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username",)
    ordering = ("username",)
    readonly_fields = (
        "passphrase",
        "Address",
        "privateKey",
        "user_profile",
    )
    filter_horizontal = ("groups", "user_permissions")


class ContactAdmin(admin.ModelAdmin):
    """This class provides the Contact endpoint for the app"""

    list_display = ["user_profile", "user", "name", "contact_address"]
    list_filter = ["user"]
    readonly_fields = ["user", "name", "contact_address"]
    exclude = [
        "profile_pic",
    ]


class Direct_messageAdmin(admin.ModelAdmin):
    """This class provides the Direct_message endpoint for the app"""

    list_display = ["User", "recipient", "date", "is_read"]
    ordering = ["-date"]
    list_filter = ["sender", "recipient"]
    readonly_fields = [
        "User",
        "sender",
        "recipient",
        "body",
        "date",
    ]


class request_tokenAdmin(admin.ModelAdmin):
    """This class provides the request_token endpoint for the app"""

    list_display = [
        "sender",
        "recipient",
        "token",
        "is_rejected",
        "is_accepted",
        "date",
    ]
    ordering = ["-date"]
    list_filter = ["User", "recipient", "is_rejected", "is_accepted"]
    readonly_fields = ["User", "sender", "recipient", "token", "date"]


class support_dmAdmin(admin.ModelAdmin):
    """This class provides the support_dm endpoint for the app"""

    list_display = ["User", "recipient", "is_read", "date"]
    ordering = ["-date"]
    list_filter = ["sender", "recipient", "is_read"]
    readonly_fields = ["User", "sender", "recipient", "body", "date"]


class NFT_dataAdmin(admin.ModelAdmin):
    list_display = ["user_profile", "User", "NFT_id", "NFT_trxn_hash"]
    list_filter = ["User"]
    readonly_fields = ["User", "NFT_id", "NFT_trxn_hash", "NFT_image"]


admin.site.unregister(Group)
admin.site.register(user, UserAdmin)
admin.site.register(Contacts, ContactAdmin)
admin.site.register(FAQs)
admin.site.register(Email_verify)
admin.site.register(admin_data)
admin.site.register(Messages, Direct_messageAdmin)
admin.site.register(TokenRequests, request_tokenAdmin)
admin.site.register(Support, support_dmAdmin)
admin.site.register(HealthRecords, NFT_dataAdmin)

UserAdmin.fieldsets += (
    (
        "More Information",
        {
            "fields": (
                "passphrase",
                "Address",
                "privateKey",
                "user_token",
                "role",
            )
        },
    ),
)
