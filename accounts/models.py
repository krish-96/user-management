from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import time
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UnixTimeStamp(models.Model):
    created_timestamp = models.BigIntegerField(null=True, blank=True)
    updated_timestamp = models.BigIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def datetime_created(self):
        return datetime.timestamp(self.created_timestamp)

    @property
    def datetime_updated(self):
        return datetime.timestamp(self.updated_timestamp)

    def save(self, *args, **kwargs):
        current_timestamp = time.time() * 1000
        if not self.created_timestamp:
            self.created_timestamp = current_timestamp
        self.updated_timestamp = current_timestamp
        super().save(*args, **kwargs)


class User(AbstractUser, UnixTimeStamp):
    account_id = models.CharField(max_length=64, unique=True, null=False, blank=False, db_index=True)
    is_email_verified = models.BooleanField(
        default=False, null=False, blank=False, help_text=_(
            "To identify whether the user email is verified or not"
        ))
    is_valid_user = models.BooleanField(
        default=False, null=False, blank=False, help_text=_(
            "To identify whether the user email is valid or not"
        ))

    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)
        super().save(*args, **kwargs)
