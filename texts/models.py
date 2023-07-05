from django.db import models
from django.conf import settings

# Create your models here.


class TextMessage(models.Model):
    textsender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="textsender")
    textreceiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="textreceiver")
    body = models.TextField(max_length=1000, null=False, blank=True, default="")
    edittime = models.DateTimeField(verbose_name="edit time", auto_now=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body
    class Meta:
        ordering = ('-edittime',)

