from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.

def get_sharedmedia_filepath(self, filename):
    return f'shared_media/{self.mediasender.pk}/%Y/%m/%d/'

class SharedMedia(models.Model):
    mediasender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mediasender")
    mediareceiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mediareceiver")
    media = models.FileField(upload_to="shared_media/", null=True, blank=True)
    edittime = models.DateTimeField(verbose_name="edit time", auto_now=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.media
    class Meta:
        ordering = ('-edittime',)
