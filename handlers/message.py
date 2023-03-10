from telethon import events
from types import NoneType
from config.language import detect_cyrillic_language, get_language
from config.catalog_API import (
    response_ru, response_uz, response_cyrl,
    get_categories
)
from pprint import pprint
import handlers.client
import json

client = handlers.client.clientHandler


@events.register(events.NewMessage(incoming=True)) #, chats=-1001763109051))
async def messages_hand(event):
    if event.is_private:
        pass
        # user = await client.get_entity(event.peer_id)
        # first = user.first_name
        # last = user.last_name if not "None" else ""
        # await event.forward_to(1578600046)
        # print('it\'s  a user')
        # raise events.StopPropagation
    else:
        if event.message.grouped_id == None:
            # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
            group = await event.message.get_chat()
            try:
                user = await event.message.get_sender()
                channel = False
                is_bot = user.bot
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
                print(fullname)
                link = user.username
                channel = True
                is_bot = False
            group_link = f'{group.title}'
            try:
                group_link = group.username
                group_link2 = f'<a href=https://t.me/{group.username}>{group.title}</a>'
            except:
                pass

            # Xabarni filtrlash boshlandi
            if event.message.text and len(event.message.text.split()) > 3 and not is_bot:
                if get_language(event.message.text):
                    lan = 'ru'
                    ctgrs = get_categories(response_ru, event.message.text)
                else:
                    if detect_cyrillic_language(event.message.text):
                        print("?????????? ???? ??????????????????")
                        lan = 'uz_cyrl'
                        ctgrs = get_categories(response_cyrl, event.message.text)

                    else:
                        print("Matn lotinchada")
                        lan = 'uz_latn'
                        ctgrs = get_categories(response_uz, event.message.text)
                
                data = dict()
                data["user_id"]=user.id
                data["fullname"]=fullname
                data["group_id"]=group.id
                data["group_title"]=group.title
                data["group_link"]=f'https://t.me/{group.username}'
                data["message_id"]=event.message.id
                data["message_text"]=event.message.text
                data["message_link"]=f'https://t.me/{group_link}/{event.message.id}'
                data["catalog_options"]=ctgrs
                data["lan"] = lan
                data = json.dumps(data, indent = 4)
                
                # print(ctgrs)
                if ctgrs != "":
                    if not channel:
                        await client.send_message(-1001578600046,
                                                  f"Statusi: Bazaga #joylandi\n"
                                                  f"User: {link2}\n"
                                                  f"Group: {group_link2}\n"
                                                  f"Catalogs:\n <code>{ctgrs}</code>\n"
                                                  f"Message: <i>{event.message.text}</i>\n"
                                                  f"message_link: https://t.me/{group_link}/{event.message.id}",
                                                  file=event.message.media,
                                                  parse_mode="Html",
                                                  link_preview=False)
                    else:
                        await client.send_message(-1001578600046,
                                                  f"Statusi: Bazaga #joylandi\n"
                                                  f"Channel: {group_link2}\n"
                                                  f"Catalogs:\n <code>{ctgrs}</code>\n"
                                                  f"Message: <i>{event.message.text}</i>\n"
                                                  f"message_link: https://t.me/{group_link}/{event.message.id}",
                                                  file=event.message.media,
                                                  parse_mode="Html",
                                                  link_preview=False)

                else:
                    if not channel:
                        await client.send_message(-1001578600046,
                                                  f"Statusi: Bazaga #joylanmadi\n"
                                                  f"User {link2}\n"
                                                  f"Group {group_link2}\n"
                                                  f"Message: <i>{event.message.text}</i>\n"
                                                  f"message_link: https://t.me/{group_link}/{event.message.id}",
                                                  file=event.message.media,
                                                  parse_mode="Html",
                                                  link_preview=False)
                    else:
                        await client.send_message(-1001578600046,
                                                  f"Statusi: Bazaga #joylanmadi\n"
                                                  f"?????????????????? ???? ???????????? {group_link2}\n"
                                                  f"Message: <i>{event.message.text}</i>\n"
                                                  f"message_link: https://t.me/{group_link}/{event.message.id}",
                                                  file=event.message.media,
                                                  parse_mode="Html",
                                                  link_preview=False)

                await client.send_message(
                    # "@demo_test_mohirdev_bot", 
                    "Tanlappbot",
                    f"{data}",
                    file=event.message.media,
                    parse_mode="Html", link_preview=False
                    )
        raise events.StopPropagation
