from django.urls import path

from account.views import (
    profileview
)

app_name = "account"

urlpatterns = [
    path('<username>/', profileview, name="view")
]
