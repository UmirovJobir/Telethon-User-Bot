from telethon import events
import os
from html_telegraph_poster.upload_images import upload_image
import handlers.client

client = handlers.client.client

@client.on(events.NewMessage(outgoing=True, pattern=r'\.hi'))
async def greeting(event):
    chat = await event.get_chat()
    # await client.send_message(chat, "Hello!!!")       #To send message in the chat
    await event.reply("Hello How are you!")  # To reply


@client.on(events.NewMessage(outgoing=True, pattern=r'\.me'))
async def aboutme(event):
    chat = await event.get_chat()
    await client.edit_message(event.message, "Hello edited!")  # To edit message


@client.on(events.NewMessage(outgoing=True, pattern=r'\.alive'))
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


@client.on(events.NewMessage(outgoing=True, pattern=r'\.tu'))
async def telegraphUploadHandler(event):
    chat = await event.get_chat()
    text = await client.edit_message(event.message, "Processing.....")
    replied = await event.get_reply_message()
    try:
        image = await replied.download_media()
        url = upload_image(image)
    except:
        return await client.edit_message(event.message, "Reply to an Image")
    await client.send_message(chat, url, link_preview=True)
    await client.delete_messages(chat, text)


client.start()
client.run_until_disconnected()
