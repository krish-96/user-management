from django.contrib import admin
from .models import User

from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

class BaseModelAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

    class Meta:
        abstract = True


class UserAdmin(BaseModelAdmin):

    list_display = (
        'username', "is_active", "is_superuser", "is_staff",
        'account_id', "email", "date_joined", "last_login",
        "first_name", "last_name", "get_full_name",
        # "is_valid_user"
    )

    # readonly_fields = ("account_id",)

    # def is_valid_user(self, obj):
    #     return obj.first_name + " " + obj.last_name

    fieldsets = [
        (
            "User Details",
            {
                "fields": [
                    ("username", "email"),
                    ("first_name", "last_name")

                ],
            },
        ),
        (
            None,
            {
                "fields": [
                    ("is_active", "is_superuser", "is_staff", "is_email_verified", "is_valid_user"),
                    # ("is_email_verified", "is_valid_user"),
                ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["account_id", "password"],
            },
        ),
    ]


admin.site.unregister(TokenProxy)

admin.site.register(User, UserAdmin)

