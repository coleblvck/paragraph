from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="User")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username



class FriendUtilities(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="utilityuser")
    requests = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="requests")
    userblocked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="blocked")


    def __str__(self):
        return self.user.username