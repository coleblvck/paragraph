"""
WSGI config for paragraph project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paragraph.settings')

application = get_wsgi_application()

from email_verification.views import delete_inactive_users

t = Thread(target=delete_inactive_users)
t.start()