from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.chat_permissions import ChatPermissions
from datetime import timedelta

import asyncio

from Python.Mak_Gripe_bot.keyboards.kb import menu_subcride
from Python.Mak_Gripe_bot.moderation.forbidden_words import WORDS
from Python.Mak_Gripe_bot.auxiliary_files.config import token_API, chanel_URL, chanel_ID, chat_ID, bot_URL



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)



def user_status_check_left(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False



bad_words = 3



async def forbidden_message(message: types.Message) -> None:
    global bad_words
    global id_user_banned
    if user_status_check_left(await bot.get_chat_member(chat_id=chanel_ID,
                                                        user_id=message.from_user.id)):
        text = message.text.lower()
        for word in WORDS:
            if word in text:
                if bad_words > 1:
                    await message.delete()
                    first_msg = await message.answer(f'Мат, флуд и прочие выражения запрещены!\n'
                                                     f'Впредь будь аккуратнее! У тебя есть ещё {bad_words} попытки.')
                    first_msg_id_message = first_msg.message_id
                    bad_words -= 1
                    await asyncio.sleep(5)
                    await bot.delete_message(chat_id=message.chat.id,
                                             message_id=first_msg_id_message)
                    await bot.restrict_chat_member(chat_id=chat_ID,
                                                   user_id=message.from_user.id,
                                                   permissions=ChatPermissions(can_send_messages=False,
                                                                               can_send_audios_notes=False,
                                                                               can_send_video_notes=False,
                                                                               can_send_media_messages=False),
                                                   until_date=timedelta(minutes=5))
                elif bad_words == 1:
                    await message.delete()
                    second_msg = await message.answer(f'Мат, флуд и прочие выражения запрещены!\n'
                                                      f'Впредь будь аккуратнее! У тебя осталась всего '
                                                      f'{bad_words} попытка.')
                    second_msg_id_message = second_msg.message_id
                    bad_words -= 1
                    await asyncio.sleep(5)
                    await bot.delete_message(chat_id=message.chat.id,
                                             message_id=second_msg_id_message)
                    await bot.restrict_chat_member(chat_id=chat_ID,
                                                   user_id=message.from_user.id,
                                                   permissions=ChatPermissions(can_send_messages=False,
                                                                               can_send_audios_notes=False,
                                                                               can_send_video_notes=False,
                                                                               can_send_media_messages=False),
                                                   until_date=timedelta(hours=1))
                elif bad_words == 0:
                    await message.delete()
                    third_msg = await message.answer(f'Как жаль!\n'
                                                     f'У тебя осталось {bad_words} попыток. Мы вынуждены '
                                                     f'с тобой попрощаться!')
                    third_msg_id_message = third_msg.message_id
                    await asyncio.sleep(5)
                    await bot.ban_chat_member(chat_id=chat_ID,
                                              user_id=message.from_user.id)
                    await bot.delete_message(chat_id=message.chat.id,
                                             message_id=third_msg_id_message)
                    bad_words = 3
                    id_user_banned = message.from_user.id
                    return id_user_banned

async def user_joined(message: types.Message) -> None:
    global id_this_message
    if user_status_check_left(await bot.get_chat_member(chat_id=chanel_ID,
                                                        user_id=message.from_user.id)):
        await bot.restrict_chat_member(chat_id=chat_ID,
                                       user_id=message.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=False,
                                                                   can_send_audios_notes=False,
                                                                   can_send_video_notes=False,
                                                                   can_send_media_messages=False),
                                       until_date=timedelta(minutes=1))
        msg_joined = await bot.send_message(text=f'<i>Приветствую тебя, <b>{message.from_user.first_name}</b> !\n\n'
                                                 f'Ты вступил в беседу "<b>{message.chat.title}'
                                                 f'</b>", где ты можешь узнать все '
                                                 f'интересующие вопросы о шинах и не только!\n\n'
                                                 f'Мы временно тебя замутили, '
                                                 f'чтобы ты смог более детально ознакомиться '
                                                 f'со всей информацией, написав нашему Telegram-боту - '
                                                 f'<a href="{bot_URL}">Mak_Gripe_bot</a>.\n'
                                                 f'Он поможет тебе подобрать товар и связаться с заказчиками, '
                                                 f'чтобы купить то, что нужно именно тебе.\n\n'
                                                 f'Удачных покупок!</i>',
                                            parse_mode='HTML',
                                            chat_id=chat_ID)
        id_msg_joined = msg_joined.message_id
        await asyncio.sleep(60)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=id_msg_joined)
    else:
        await bot.restrict_chat_member(chat_id=chat_ID,
                                       user_id=message.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=False,
                                                                   can_send_audios_notes=False,
                                                                   can_send_video_notes=False,
                                                                   can_send_media_messages=False),
                                       until_date=timedelta(seconds=15))
        msg = await bot.send_message(text=f'<i>Приветствую тебя, <b>{message.from_user.first_name}</b>!\n\n'
                                          f'Ты вступил в беседу "<b>{message.chat.title}</b>", '
                                          f'где ты можешь узнать все '
                                          f'интересующие вопросы о шинах и не только!\n\n'
                                          f'Ты не можешь писать? Конечно!\n'
                                          f'Ведь перед этим ты должен подписаться на наш '
                                          f'<a href="{chanel_URL}">Telegram-канал</a></i>!\n',
                                     parse_mode='HTML',
                                     reply_markup=menu_subcride,
                                     chat_id=chat_ID)
        id_this_message = msg.message_id
        return id_this_message

async def user_is_not_subscribed(message: types.Message) -> None:
    if user_status_check_left(await bot.get_chat_member(chat_id=chanel_ID,
                                                        user_id=message.from_user.id)):
        await bot.restrict_chat_member(chat_id=chat_ID,
                                       user_id=message.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=True,
                                                                   can_send_polls=True,
                                                                   can_send_other_messages=True,
                                                                   can_send_media_messages=True),
                                       until_date=timedelta(seconds=15))
        await bot.restrict_chat_member(chat_id=chat_ID,
                                       user_id=message.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=False,
                                                                   can_send_audios_notes=False,
                                                                   can_send_video_notes=False,
                                                                   can_send_media_messages=False),
                                       until_date=timedelta(seconds=30))
        await bot.delete_message(chat_id=chat_ID,
                                 message_id=id_this_message)
        msd_introductory_inf = await bot.send_message(text=f'<i>Отлично!\n'
                                                           f'Ты подписался на наш Telegram-канал "<a href="{chanel_URL}'
                                                           f'"><b>MakGripe | МакГрайп</b></a>"!\n\n'
                                                           f'Если ты захочешь пробрести себе какой-то товар, то напиши'
                                                           f'нашему Telegram-боту - <a href="{bot_URL}">'
                                                           f'Mak_Gripe_bot</a>.\n'
                                                           f'Он с радостью поможет тебе подобрать его '
                                                           f'и связаться с заказчиками.\n\n'
                                                           f'Удачных покупок!</i>',
                                                      parse_mode='HTML',
                                                      chat_id=chat_ID)
        id_msd_introductory_inf = msd_introductory_inf.message_id
        await asyncio.sleep(30)
        await bot.delete_message(chat_id=chat_ID,
                                 message_id=id_msd_introductory_inf)
    else:
        await bot.restrict_chat_member(chat_id=chat_ID,
                                       user_id=message.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=False,
                                                                   can_send_polls=False,
                                                                   can_send_other_messages=False,
                                                                   can_send_media_messages=False),
                                       until_date=timedelta(seconds=15))



def register_handlers_moderation(dp: Dispatcher) -> None:
    dp.register_message_handler(forbidden_message)
    dp.register_message_handler(user_joined,
                                content_types=['new_chat_members'])
    dp.register_callback_query_handler(user_is_not_subscribed,
                                       text='userisntsubcribed')
