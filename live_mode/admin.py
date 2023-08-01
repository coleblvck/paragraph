from django.contrib import admin
from .models import NowPlaying

# Register your models here.
class NowPlayingAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = NowPlaying
admin.site.register(NowPlaying, NowPlayingAdmin)