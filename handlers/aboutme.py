from telethon import events
import handlers.client

client = handlers.client.clientHandler


@events.register(events.NewMessage(outgoing=True, pattern=r'\.me'))
async def aboutmeHandler(event):
    chat = await event.get_chat()
    await client.edit_message(event.message, "Hello edited!")  # To edit message
