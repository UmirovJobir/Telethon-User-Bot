from html_telegraph_poster.upload_images import upload_image
import os
from telethon import events
import handlers.client

client = handlers.client.clientHandler


@events.register(events.NewMessage(outgoing=True, pattern=r'\.tu'))
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
    await client.edit_message(event.message, "Done✅")
    os.remove(image)

