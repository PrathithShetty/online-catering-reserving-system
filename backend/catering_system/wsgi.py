"""
WSGI config for catering_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catering_system.settings')

application = get_wsgi_application()

# Vercel's Python (@vercel/python) WSGI builder looks for a module-level
# variable named `app` — Django's own tooling only ever uses `application`,
# so this alias is purely for the deployment platform.
app = application
