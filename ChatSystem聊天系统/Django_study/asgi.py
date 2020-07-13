"""
ASGI config for Django_study project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from websocket import websocket_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_study.settings')

http_application = get_asgi_application()

async def application(scope,receive,send):
    # await http_application(scope,receive,send)
    # print('scopr:',scope)
    if scope['type']=='http':
        await http_application(scope,receive,send)
    elif scope['type']=='webscoket':
        await websocket_application(scope,receive,send)
    else:
        raise Exception("uknown scope type,"+scope['type'])