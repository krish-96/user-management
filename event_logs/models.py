from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User, UnixTimeStamp


# Create your models here.

class EventLog(UnixTimeStamp):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('GET', 'Get'),
        ('LIST', 'List'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAIL', 'Fail'),
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=128, blank=False, null=False, db_index=True,
                                  help_text=_("Model name tried to access or update"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    url_path = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        # return f"{self.action} - {self.model_name} {self.object_id} - {self.status}"
        return f"{self.status}: {self.message}"


class UserLoginEvents(UnixTimeStamp):

    """
    The sample for user login data:
    {
    "id": 7,
    "created_timestamp": 1734594633732,
    "updated_timestamp": 1734594633732,
    "is_success": false,
    "reason": "User Not Found with the provided username",
    "user_data": {
        "ip": "127.0.0.1",
        "username": "Krishna1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "request_method": "POST",
        "headers": {
            "content_type": "application/json",
            "accept_language": "en-US,en;q=0.9"
        },
        "geo_location": {
            "country": "United States",
            "city": "San Francisco",
            "region": "California"
        }
    },
    "user": null,
    "additional_metadata": {
        "device_type": "Desktop",
        "browser": "Chrome",
        "login_attempt_number": 3,
        "previous_failed_attempts": [
            {
                "timestamp": 1734594000000,
                "ip": "192.168.0.101",
                "reason": "Invalid password"
            }
        ]
    }
}

    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    is_success = models.BooleanField(default=False)
    reason = models.CharField(max_length=256, blank=True, null=True)
    user_data = models.JSONField(verbose_name="user details", blank=True, null=True)


    def __repr__(self):
        return f"{self.user.username if isinstance(self.user, User) else 'Unknown User'}"

    def __str__(self):
        return f"{self.user.username if isinstance(self.user, User) else 'Unknown User'}"
