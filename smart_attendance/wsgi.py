"""
WSGI config for smart_attendance project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# Ensure this matches your project settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_attendance.settings")

application = get_wsgi_application()
