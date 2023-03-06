from telethon import events


@events.register(events.NewMessage(outgoing=True, pattern=r'\.hi'))
async def greetingHandler(event):
    chat = await event.get_chat()
    # await client.send_message(chat, "Hello!!!")       #To send message in the chat
    await event.reply("Hello How are you!")  # To reply
