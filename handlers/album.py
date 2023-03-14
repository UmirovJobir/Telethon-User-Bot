from telethon import events
from types import NoneType
from aiogram.utils.deep_linking import decode_payload
from config.language import detect_cyrillic_language, get_language
from config.catalog_API import (
    response_ru, response_uz, response_cyrl,
    get_categories
)
import json
import handlers.client

client = handlers.client.clientHandler


@events.register(events.Album(chats=-1001763109051))
async def albumHandler(event):
    # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
    # print(event)

    group = await event.original_update.message.get_chat()
    print(event.original_update.message.id)
    try:
        user = await event.original_update.message.get_sender()
        channel = False
        first_name = user.first_name
        last_name = user.last_name if type(user.last_name) != NoneType else ""
        fullname = f"{first_name} {last_name}"
        print(fullname)
        try:
            if type(user.phone) == NoneType:
                raise Exception
            link = user.phone
            link2 = f"<a href=https://t.me/+{user.phone}>{fullname}</a>"
        except:
            try:
                if type(user.username) == NoneType:
                    raise Exception

                link = user.username
                link2 = f"<a href=https://t.me/{user.username}>{fullname}</a>"
            except:
                link = 'none'
                link2 = fullname
    except:
        fullname = user.title
        link = user.username
        channel = True
    group_link = f'{group.title}'
    try:
        group_link = group.username
        group_link2 = f'<a href=https://t.me/{group.username}>{group.title}</a>'
    except:
        pass
    # Xabarni filtrlash boshlandi
    # print(event.text)
    # print(event.raw_text)
    
    if get_language(event.text):
        lan = 'ru'
        ctgrs = get_categories(response_ru, event.text)
    else:
        if detect_cyrillic_language(event.text):
            print("Текст на кириллице")
            lan = 'uz_cyrl'
            ctgrs = get_categories(response_cyrl, event.text)

        else:
            print("Matn lotinchada")
            lan = 'uz_latn'
            ctgrs = get_categories(response_uz, event.text)

    data = dict()
    data["user_id"]=user.id
    data["fullname"]=fullname
    data["group_id"]=group.id
    data["group_title"]=group.title
    data["group_link"]=f'https://t.me/{group.username}'
    data["message_id"]=event.original_update.message.id
    data["message_text"]=event.text
    data["message_link"]=f'https://t.me/{group_link}/{event.original_update.message.id}'
    data["catalog_options"]=ctgrs
    data["lan"] = lan
    data = json.dumps(data)

    # print(ctgrs)
    if ctgrs != "":
        if not channel:
            await client.send_message(-1001578600046,
                                        f"Statusi: Bazaga #joylandi\n"
                                        f"User: {link2}\n"
                                        f"Group: {group_link2}\n"
                                        f"Catalogs:\n <code>{ctgrs}</code>\n"
                                        f"Message: <i>{event.text}</i>\n"
                                        f"message_link: https://t.me/{group_link}/{event.original_update.message.id}",
                                        file=event.messages,
                                        parse_mode="Html",
                                        link_preview=False)
        else:
            await client.send_message(-1001578600046,
                                        f"Statusi: Bazaga #joylandi\n"
                                        f"Channel: {group_link2}\n"
                                        f"Catalogs:\n <code>{ctgrs}</code>\n"
                                        f"Message: <i>{event.text}</i>\n"
                                        f"message_link: https://t.me/{group_link}/{event.original_update.message.id}",
                                        file=event.messages,
                                        parse_mode="Html",
                                        link_preview=False)

    else:
        if not channel:
            await client.send_message(-1001578600046,
                                        f"Statusi: Bazaga #joylanmadi\n"
                                        f"User {link2}\n"
                                        f"Group {group_link2}\n"
                                        f"Message: <i>{event.text}</i>\n"
                                        f"message_link: https://t.me/{group_link}/{event.original_update.message.id}",
                                        file=event.messages,
                                        parse_mode="Html",
                                        link_preview=False)
        else:
            await client.send_message(-1001578600046,
                                        f"Statusi: Bazaga #joylanmadi\n"
                                        f"Сообщение от канала {group_link2}\n"
                                        f"Message: <i>{event.text}</i>\n"
                                        f"message_link: https://t.me/{group_link}/{event.original_update.message.id}",
                                        file=event.messages,
                                        parse_mode="Html",
                                        link_preview=False)
    await client.send_message(
        # "@demo_test_mohirdev_bot",
        "@Tanlappbot",  #output 
        message=f"{data}", #caption
        file=event.messages, #list of messages
    )

    await client.send_message(
        "@demo_test_mohirdev_bot",
        message=f"{data}", #caption
        file=event.messages, #list of messages
    )

    raise events.StopPropagation