from django.db import models
from django.conf import settings

# Create your models here.

class FCMToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="FCMUser")
    token = models.TextField(max_length=250, null=True, blank=True, default="")
    
    def __str__(self):
        return self.token



