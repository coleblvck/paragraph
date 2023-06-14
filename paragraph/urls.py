"""
URL configuration for paragraph project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import registerview, logoutview, loginview, profileview, profileupdate
from graph.views import index
from texts.views import chat, textsview, sentmessages, receivedmessages, textsscreen
from friendships.views import friendsrequestsview

urlpatterns = [
    path('', index, name="home"),
    path('admin/', admin.site.urls),
    path('chat/<friend>', chat, name="chat"),
    path('texts', textsview, name="textsview"),
    path('get-started', registerview, name="register"),
    path('logout', logoutview, name="logoutview"),
    path('login', loginview, name="loginview"),
    # API Views
    path('sent_msg/<friend>', sentmessages, name="sent_msg"),
    path('received_msg/<friend>', receivedmessages, name="received_msg"),
    path('textsscreen', textsscreen, name="textsscreen"),
    #
    path('user/', include('account.urls', namespace="user")),
    path('update', profileupdate, name="update"),
    path('requests', friendsrequestsview, name="friendsrequestsview")
    #path('', include("graph.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)