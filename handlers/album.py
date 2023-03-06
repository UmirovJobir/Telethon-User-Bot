from telethon import events
from types import NoneType
import handlers.client

client = handlers.client.clientHandler


@events.register(events.Album())
async def albumHandler(event):
    # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
    # print(event)

    group = await event.original_update.message.get_chat()
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
    data = f"""{user.id}(delimeter){fullname}(delimeter){link}(delimeter){group.id}(delimeter){group.title}(delimeter){group_link}(delimeter){event.messages[0].id}(delimeter){event.text}"""

    await client.send_message(
        "@demo_test_mohirdev_bot",  # output
        message=data,  # caption
        file=event.messages,  # list of messages
    )
    raise events.StopPropagation