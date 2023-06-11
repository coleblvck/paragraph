from django.contrib import admin
from .models import FriendUtilities, FriendList

# Register your models here.



class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(FriendList, FriendListAdmin)


class FriendUtilitiesAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']

    class Meta:
        model = FriendUtilities

admin.site.register(FriendUtilities, FriendUtilitiesAdmin)
