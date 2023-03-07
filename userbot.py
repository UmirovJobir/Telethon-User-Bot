from telethon import events

from types import NoneType
import logging

import handlers.client
import handlers.greeting
import handlers.alive
import handlers.telegraph
import handlers.aboutme
import handlers.quto
import handlers.album
import handlers.message

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#                     level=logging.INFO)


client = handlers.client.clientHandler

with client as dracula:
    dracula.add_event_handler(handlers.greeting.greetingHandler)

with client as dracula:
    dracula.add_event_handler(handlers.alive.aliveHandler)

with client as dracula:
    dracula.add_event_handler(handlers.telegraph.telegraphUploadHandler)

with client as dracula:
    dracula.add_event_handler(handlers.aboutme.aboutmeHandler)

with client as dracula:
    dracula.add_event_handler(handlers.quto.qutoHandler)

# with client as dracula:
#     dracula.add_event_handler(handlers.album.albumHandler)

with client as dracula:
    dracula.add_event_handler(handlers.message.messages_hand)


client.start()
client.run_until_disconnected()
