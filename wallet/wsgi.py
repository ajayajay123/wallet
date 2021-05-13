"""
WSGI config for wallet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from walletapp import views, blockchain_api
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet.settings')

application = get_wsgi_application()
print("Application Started")
views.setup()
# thread = Thread(target=blockchain_api.start_web_socket)
# thread.start()
