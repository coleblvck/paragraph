from django.db import models
from django.conf import settings

# Create your models here.
class Note(models.Model):
    notekey = models.AutoField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.CharField(max_length=100, null=True, blank=True, default="")
    body = models.TextField(max_length=1000, null=False, blank=True, default="")
    edittime = models.DateTimeField(verbose_name="edit time", auto_now=True)

    def __str__(self):
        return self.body
    class Meta:
        ordering = ('-edittime',)

class Paragraph(models.Model):
    paragraphkey = models.AutoField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.CharField(max_length=100, null=True, blank=True, default="")
    body = models.TextField(max_length=1000, null=False, blank=True, default="")
    edittime = models.DateTimeField(verbose_name="edit time", auto_now=True)

    def __str__(self):
        return self.body
    class Meta:
        ordering = ('-edittime',)