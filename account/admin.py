from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from django.apps import apps

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('user_id', 'date_joined', 'last_login')

    # Set due to errors requesting for filters
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)