from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from auxiliary_files.config import token_API, ADMIN
from keyboards.kb import kb_products, kb_menu_admin, kb_menu

import sqlite3



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)



async def start_command(message: types.Message) -> None:
    user_id = message.from_user.id
    if user_id == ADMIN:
        await bot.send_message(chat_id=ADMIN,
                               text=f'<i>Привет, <b>Дмитрий</b>!\nЧем могу быть тебе полезен?</i>',
                               reply_markup=kb_menu_admin,
                               parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i><b>Привет!</b>\nЧем могу быть полезен?</i>',
                               reply_markup=kb_menu,
                               parse_mode="HTML")

async def create_post(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Хорошо!\n\n'
                                f'Пост какого именно товара ты хочешь создать?</i>',
                           reply_markup=kb_products,
                           parse_mode='HTML')


async def all_applications(message: types.Message) -> None:
    con = sqlite3.connect('Mak_Gripe_bot\\sql\\database.db')
    with con:
        cur = con.cursor()
        send_all_applications = cur.execute('SELECT * from applications').fetchall()
        for application in send_all_applications:
            await bot.send_message(chat_id=ADMIN,
                                   text=f'<i><b>Новая заявка от пользователя</b></i>\n\n'
                                        f'<i>Имя пользователя:</i> <a href="https://t.me/{application[2][1:]}'
                                        f'">{application[2]}</a>\n\n'
                                        f'<i>Тип товара:</i> {application[1]}\n'
                                        f'<i>Артикул товара:</i> {application[3]}\n'
                                        f'<i>Кол-во оставшихся комплектов:</i> {application[6]}\n\n'
                                        f'<i>Сообщение для тебя:</i> {application[4]}\n\n'
                                        f'<i>Время создания заявки:</i> <u>{application[5]}</u>',
                                   parse_mode='HTML')


def register_handlers_dialogue_admin(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command,
                                commands=['start'])
    dp.register_message_handler(all_applications,
                                Text(equals='Посмотреть все заявки',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(create_post,
                                Text(equals='Создать новый пост',
                                     ignore_case=True),
                                state=None)
