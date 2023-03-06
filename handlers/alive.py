from telethon import events
import handlers.client

client = handlers.client.clientHandler


@events.register(events.NewMessage(outgoing=True, pattern=r'\.alive'))
async def aliveHandler(event):
    chat = await event.get_chat()
    # await client.send_message(chat, "Yes Your bot is running")
    photo = await client.get_profile_photos('me')
    me = await client.get_me()
    try:
        await client.send_file(chat, file=photo,
                               caption=
                               "I am Alive.\n\n"
                               "Owner [Jobir](https://t.me/{})\n"
                               "Channel [Mohirdev kanal](https://t.me/{})\n".format(me.username, 'jobirtestchannel')
                               )
    except TypeError:
        await client.send_message(chat, "You don't have photo")
