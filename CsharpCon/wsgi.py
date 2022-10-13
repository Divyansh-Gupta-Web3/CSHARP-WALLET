"""This module is the application callable
which the application server uses to communicate with your code"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CsharpCon.settings")

application = get_wsgi_application()
