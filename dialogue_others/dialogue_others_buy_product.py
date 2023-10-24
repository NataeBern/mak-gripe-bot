from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Python.Mak_Gripe_bot.auxiliary_files.config import token_API, chanel_URL, provider_token, ADMIN, chanel_ID
from Python.Mak_Gripe_bot.keyboards.kb import cb, kb_menu, kb_cancel, kb_application, kb_type_product
from Python.Mak_Gripe_bot.sql.sqlite import create_application, edit_application

import re
from datetime import datetime
import sqlite3



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)

con = sqlite3.connect('Mak_Gripe_bot\\sql\\database.db')
cur = con.cursor()


class ApplicationFromUser(StatesGroup):
    time = State()
    type_product = State()
    article = State()
    username = State()
    message = State()


dog_sign = re.compile('@')
article = 0



async def cancel_command(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Как скажете!\n'
                                f'Чем ещё могу быть полезен?</i>',
                           reply_markup=kb_menu,
                           parse_mode='HTML')
    await state.finish()

async def submit_application(message: types.Message, state: FSMContext) -> None:
    global time_msg, all_articles_tires, all_articles_wheels
    all_articles_tires = cur.execute('SELECT article FROM tires').fetchall()
    all_articles_wheels = cur.execute('SELECT article FROM wheels').fetchall()
    if (len(all_articles_tires) == 0 and len(all_articles_wheels) == 0):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Упссс... А все товары-то закончились...\n\n'
                                    f'Прости, но я не могу тебе пока что-нибудь предложить.\n'
                                    f'Могу я помочь чем-нибудь ещё?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
    else:
        await ApplicationFromUser.time.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Отлично!\n\n'
                                    f'Для этого тебе потребуется оставить платную заявку, '
                                    f'по которой с тобой свяжутся для обсуждения деталей в самое ближайшее время.\n\n'
                                    f'Также будет необходимо сообщить следующее:\n'
                                    f'<b> • </b>Ник в телеграмме;\n'
                                    f'<b> • </b>Артикул товара\n'
                                    f'<b> • </b>Вопрос или уточняющая информация для заказчика.\n\n'
                                    f'Почему нужно платить, чтобы оставить заявку? '
                                    f'Потому что таким способом ты бронируешь за собой место'
                                    f'и выбранный тобой товар числится уже за тобой, в количестве одного комплекта.\n\n'
                                    f'Если всё понятно и ты согласен с условиями, то давай продолжим?</i> 😉',
                               reply_markup=kb_application,
                               parse_mode="HTML")
        time_msg = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await create_application(user_id=message.from_user.id)
        return time_msg, all_articles_tires, all_articles_wheels

async def save_time_application(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_application:
        data_application['time'] = time_msg
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Ура! Я так рад!</i>',
                           reply_markup=kb_cancel,
                           parse_mode='HTML')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Давай теперь ты выберешь тот вид товара, '
                                f'который ты хочешь приобрести, нажав на соответствующую кнопку.</i>',
                           reply_markup=kb_type_product,
                           parse_mode='HTML')
    await ApplicationFromUser.next()

async def save_callback_query_tires_application(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    if len(all_articles_tires) == 0:
        current_state = await state.get_state()
        if current_state is None:
            return
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'<i>Упссс... А данный вид товаров закончился...\n\n'
                                    f'Прости, но я не могу тебе пока ничего предложить.\n'
                                    f'Могу я помочь чем-нибудь ещё?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
        await state.finish()
    else:
        kb_articles_tires = types.InlineKeyboardMarkup(row_width=2)
        for article in range(len(all_articles_tires)):
            one_article_tires = all_articles_tires[article][0]
            kb_articles_tires.add(types.InlineKeyboardButton(text=f'{one_article_tires}',
                                                             callback_data=cb.new(msg_text=f'{one_article_tires}')))
        async with state.proxy() as data_application:
            data_application['type_product'] = 'Легковые шины'
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'<i>Что ж... А теперь выбери артикул товара, который ты хочешь купить.</i>',
                               reply_markup=kb_articles_tires,
                               parse_mode='HTML')
        await ApplicationFromUser.next()

async def save_callback_query_wheels_application(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    if len(all_articles_wheels) == 0:
        current_state = await state.get_state()
        if current_state is None:
            return
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'<i>Упссс... А данный вид товаров закончился...\n\n'
                                    f'Прости, но я не могу тебе пока ничего предложить.\n'
                                    f'Могу я помочь чем-нибудь ещё?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
        await state.finish()
    else:
        kb_articles_wheels = types.InlineKeyboardMarkup(row_width=2)
        for article in range(len(all_articles_wheels)):
            one_article_wheels = all_articles_wheels[article][0]
            kb_articles_wheels.add(types.InlineKeyboardButton(text=f'{one_article_wheels}',
                                                              callback_data=cb.new(msg_text=f'{one_article_wheels}')))
        async with state.proxy() as data_application:
            data_application['type_product'] = 'Литые диски'
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'<i>Что ж... А теперь выбери артикул товара, который ты хочешь купить.\n'
                                    f'Учти, что если ты не находишь артикул товара, который есть на нашем '
                                    f'<a href="{chanel_URL}">Telegram-канал</a>, '
                                    f'то это значит, что данный товар уже закончился.</i>',
                               reply_markup=kb_articles_wheels,
                               parse_mode='HTML')
        await ApplicationFromUser.next()

async def save_article_callback_handler_application(callback_query: types.CallbackQuery,
                                                    state: FSMContext,
                                                    callback_data: dict):
    global article
    async with state.proxy() as data_application:
        article = callback_data['msg_text']
        data_application['article'] = article
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f'<i>Принято!\n'
                                f'А сейчас напиши мне своё имя пользователя, указав вначале знак "@".</i>',
                           reply_markup=kb_cancel,
                           parse_mode='HTML')
    await ApplicationFromUser.next()
    return article

async def check_username_application(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Ты забыл указать в начале знак "@"!\n\n'
                                f'Давай ты попробуешь снова?</i>',
                           reply_markup=kb_cancel,
                           parse_mode='HTML')

async def save_username_application(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_application:
        data_application['username'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Отлично!\n'
                                f'Теперь расскажи мне, чтобы ты хотел передать заказчикам в качестве информации.</i>',
                           reply_markup=kb_cancel,
                           parse_mode='HTML')
    await ApplicationFromUser.next()

async def save_message_application(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_application:
        data_application['message'] = message.text
        await bot.send_invoice(chat_id=message.chat.id,
                               title='Оставить заявку',
                               description='Тестовый формат оплаты',
                               payload='Test payment format',
                               provider_token=provider_token,
                               currency='rub',
                               prices=[types.LabeledPrice(label='Цена оплаты заявки',
                                                          amount=10000),
                                       types.LabeledPrice(label='НДС',
                                                          amount=5000)],
                               max_tip_amount=5000,
                               suggested_tip_amounts=[1000, 2000, 3000, 4000],
                               start_parameter='payment_of_the_application',
                               provider_data=None,
                               photo_url='https://images.unsplash.com/photo-1637169797848-12431f1d355c?ixlib=rb-4.0.'
                                         '3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit'
                                         '=crop&w=1964&q=80',
                               photo_size=100,
                               photo_width=800,
                               photo_height=450,
                               need_name=False,
                               need_phone_number=False,
                               need_email=False,
                               need_shipping_address=False,
                               send_phone_number_to_provider=False,
                               send_email_to_provider=False,
                               is_flexible=False,
                               disable_notification=False,
                               protect_content=False,
                               reply_to_message_id=None,
                               allow_sending_without_reply=True,
                               reply_markup=None)

async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)

async def successful_payment_save_time_application(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_application:
        if data_application['type_product'] == 'Легковые шины':
            one_number_of_sets = cur.execute(
                'SELECT number_of_sets FROM tires WHERE article == "{article}"'.format(article=article)
            ).fetchone()
            select_msg_chanel_id = cur.execute(
                'SELECT msg_chanel_id FROM tires WHERE article == "{article}"'.format(article=article)
            ).fetchone()
            if one_number_of_sets[0] == '1':
                cur.execute(
                    'DELETE FROM tires WHERE article == "{article}" AND number_of_sets = "1"'.format(article=article)
                )
                await bot.delete_message(chat_id=chanel_ID,
                                         message_id=select_msg_chanel_id[0])
            else:
                cur.execute(
                    'UPDATE tires SET number_of_sets = "{number_of_sets}" WHERE article == "{article}"'.format(
                        number_of_sets=int(one_number_of_sets[0]) - 1,
                        article=article
                    )
                )
        elif data_application['type_product'] == 'Литые диски':
            one_number_of_sets = cur.execute(
                'SELECT number_of_sets FROM wheels WHERE article == "{article}"'.format(article=article)
            ).fetchone()
            select_msg_chanel_id = cur.execute(
                'SELECT msg_chanel_id FROM wheels WHERE article == "{article}"'.format(article=article)
            ).fetchone()
            if one_number_of_sets[0] == '1':
                cur.execute(
                    'DELETE FROM wheels WHERE article == "{article}" AND number_of_sets = "1"'.format(article=article)
                )
                await bot.delete_message(chat_id=chanel_ID,
                                         message_id=select_msg_chanel_id[0])
            else:
                cur.execute(
                    'UPDATE wheels SET number_of_sets = "{number_of_sets}" WHERE article == "{article}"'.format(
                        number_of_sets=int(one_number_of_sets[0]) - 1,
                        article=article
                    )
                )
                cur.execute(
                    'UPDATE applications SET remaining_sets = "{remaining_sets}" WHERE user_id == "{user_id}"'.format(
                        remaining_sets=int(one_number_of_sets[0]) - 1, user_id=message.from_user.id
                    )
                )
    async with state.proxy() as data_application:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Спасибо за оплату <b>{message.successful_payment.total_amount // 100} '
                                    f'{message.successful_payment.currency}</b>\n\n'
                                    f'Твоя заявка сохранена и передана заказчикам. '
                                    f'Они свяжутся с тобой в ближайшее время!</i>',
                               parse_mode='HTML')
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Скажи, я могу ещё тебе чем-нибудь помочь?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
        if one_number_of_sets[0] == '1':
            await bot.send_message(chat_id=ADMIN,
                                   text=f'<i><b>Новая заявка от пользователя</b></i>\n\n'
                                        f'<i>Имя пользователя:</i> <a href="https://t.me/{data_application["username"][1:]}'
                                        f'">{data_application["username"]}</a>\n\n'
                                        f'<i>Тип товара:</i> {data_application["type_product"]}\n'
                                        f'<i>Артикул товара:</i> {article}\n'
                                        f'<i>Кол-во оставшихся комплектов:</i> 0\n\n'
                                        f'<i>Сообщение для тебя:</i> {data_application["message"]}\n\n'
                                        f'<i>Время создания заявки:</i> <u>{data_application["time"]}</u>',
                                   parse_mode='HTML', )
        else:
            await bot.send_message(chat_id=ADMIN,
                                   text=f'<i><b>Новая заявка от пользователя</b></i>\n\n'
                                        f'<i>Имя пользователя:</i> <a href="https://t.me/{data_application["username"][1:]}'
                                        f'">{data_application["username"]}</a>\n\n'
                                        f'<i>Тип товара:</i> {data_application["type_product"]}\n'
                                        f'<i>Артикул товара:</i> {article}\n'
                                        f'<i>Кол-во оставшихся комплектов:</i> {int(one_number_of_sets[0]) - 1}\n\n'
                                        f'<i>Сообщение для тебя:</i> {data_application["message"]}\n\n'
                                        f'<i>Время создания заявки:</i> <u>{data_application["time"]}</u>',
                                   parse_mode='HTML',)
    await edit_application(state=state, user_id=message.from_user.id)
    await state.finish()



def register_handlers_dialogue_others_buy_pr(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_command,
                                Text(equals='В начало меню',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(submit_application,
                                Text(equals='Хочу купить товар!',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(save_time_application,
                                Text(equals='Да, давай!',
                                     ignore_case=True),
                                state=ApplicationFromUser.time)
    dp.register_callback_query_handler(save_callback_query_tires_application,
                                       lambda callback_query: callback_query.data == 'passenger_tires',
                                       state=ApplicationFromUser.type_product)
    dp.register_callback_query_handler(save_callback_query_wheels_application,
                                       lambda callback_query: callback_query.data == 'cast_wheels',
                                       state=ApplicationFromUser.type_product)
    dp.register_callback_query_handler(save_article_callback_handler_application,
                                       cb.filter(),
                                       state=ApplicationFromUser.article)
    dp.register_message_handler(check_username_application,
                                lambda message: not dog_sign.match(message.text),
                                state=ApplicationFromUser.username)
    dp.register_message_handler(save_username_application,
                                state=ApplicationFromUser.username)
    dp.register_message_handler(save_message_application,
                                state=ApplicationFromUser.message)
    dp.register_pre_checkout_query_handler(pre_checkout_query,
                                           lambda query: True,
                                           state=ApplicationFromUser.message)
    dp.register_message_handler(successful_payment_save_time_application,
                                content_types=types.ContentType.SUCCESSFUL_PAYMENT,
                                state=ApplicationFromUser.message)
