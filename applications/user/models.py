from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    subsonic_api_token = models.CharField(blank=True, null=True, max_length=255)
