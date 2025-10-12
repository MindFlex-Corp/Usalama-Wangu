"""
WSGI config for Usalama_Wangu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Usalama_Wangu.settings') # For development
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.Usalama_Wangu.settings') # For deployment

application = get_wsgi_application()
