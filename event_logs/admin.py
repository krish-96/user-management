from django.contrib import admin
from .models import EventLog, UserLoginEvents
from accounts.admin import BaseModelAdmin
from accounts.models import User


# Register your models here.

class EventLogAdmin(BaseModelAdmin):
    model = EventLog
    raw_id_fields = ["user"]

    def has_delete_permission(self, request, obj=None):
        return False


class UserLoginEventsAdmin(BaseModelAdmin):
    model = UserLoginEvents
    list_display = ['get_user', 'is_success', 'get_reason']
    raw_id_fields = ['user']
    list_filter = ['user']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_user(self, obj):
        print(f"Called: {obj} | {type(obj)}")
        return f"{obj.user.username if isinstance(obj.user, User) else 'Unknown User'}"


    def get_reason(self, obj):
        print(f"Called: {obj} | {type(obj.user_data)}")
        username = obj.user_data.get('username') if obj.user_data and 'username' in obj.user_data else ''
        return f"{obj.reason}{ f' ({username})' if username else ''}"


admin.site.register(EventLog, EventLogAdmin)
admin.site.register(UserLoginEvents, UserLoginEventsAdmin)
