from django.db import models
from django.conf import settings

# Create your models here.

class NowPlaying(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    switch = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    title = models.CharField(max_length=100, null=True, blank=True, default="")
    artist = models.CharField(max_length=100, null=True, blank=True, default="")
    album = models.CharField(max_length=100, null=True, blank=True, default="")
    progress = models.DecimalField(null=True, blank=True, default=0.0, decimal_places=5, max_digits=6)
    listentime = models.DateTimeField(verbose_name="listen time", auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-listentime',)
