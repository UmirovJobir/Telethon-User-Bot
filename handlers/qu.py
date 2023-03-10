from telethon import events
import handlers.client

client = handlers.client.clientHandler


@events.register(events.NewMessage(outgoing=True, pattern=r'\.q'))
async def qutoHandler(event):
    chat = await event.get_chat()
    repplied_msg = await event.get_reply_message()
    x = await repplied_msg.forward_to('@demo_test_mohirdev_bot')
    print(event.message.id)
    print(x)
    async with client.conversation('@demo_test_mohirdev_bot') as conv:
        xx = await conv.get_response(x.id)
        await client.send_read_acknowledge(conv.chat_id)   #no notification
        # await client.send_message(chat, xx)
        await event.message.delete()
