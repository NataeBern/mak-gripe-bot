from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Python.Mak_Gripe_bot.auxiliary_files.config import token_API
from Python.Mak_Gripe_bot.keyboards.kb import cb_pick_up, kb_products_pick_up, kb_tire_parameters, kb_menu, \
    kb_wheels_parameters

import sqlite3



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)

con = sqlite3.connect('Mak_Gripe_bot\\sql\\database.db')
cur = con.cursor()


class ProductSelection(StatesGroup):
    tires_width = State()
    tires_height = State()
    tires_diameter = State()
    wheels_rim_width = State()
    wheels_diameter = State()
    wheels_departure = State()





async def pick_up_product(message: types.Message) -> None:
    global all_articles_tires, all_articles_wheels
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
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Хорошо!\n'
                                    'Тогда нажми на кнопку, на которой написано '
                                    'по конкретно чему ты хочешь осуществить подбор.</i>',
                               reply_markup=kb_products_pick_up,
                               parse_mode='HTML')
    return all_articles_tires, all_articles_wheels

async def pick_up_product_tires(message: types.Message) -> None:
    if len(all_articles_tires) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Упссс... А данный вид товаров закончился...\n\n'
                                    f'Прости, но я не могу тебе пока ничего предложить.\n'
                                    f'Могу я помочь чем-нибудь ещё?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Принято! Шины, так шины.\n'
                                    'Теперь выбери по какому параметру тебе важно найти свой товар '
                                    'и я тебе следующим сообщением вышлю их варианты.</i>',
                               reply_markup=kb_tire_parameters,
                               parse_mode='HTML')

async def pick_up_product_tires_width(message: types.Message) -> None:
    all_width_tires = cur.execute('SELECT width FROM tires').fetchall()
    kb_width_tires = types.InlineKeyboardMarkup(row_width=2)
    for width in range(len(all_width_tires)):
        one_width_tires = all_width_tires[width][0]
        kb_width_tires.add(types.InlineKeyboardButton(text=f'{one_width_tires}',
                                                      callback_data=cb_pick_up.new(msg_pick_up=f'{one_width_tires}')))
    await ProductSelection.tires_width.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_width_tires,
                           parse_mode='HTML')

async def send_pick_up_product_tires_width(callback_query: types.CallbackQuery,
                                           callback_data: dict,
                                           state: FSMContext) -> None:
    async with state.proxy():
        width = callback_data['msg_pick_up']
        send_all_tires_width = cur.execute(
            'SELECT * from tires WHERE width == "{width}"'.format(width=width)
        ).fetchall()
        for tires_width in send_all_tires_width:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=tires_width[1],
                                 caption=f'<b>{tires_width[2]} {tires_width[3]} '
                                         f'{tires_width[4]}/{tires_width[5]} D{tires_width[6]} '
                                         f'{tires_width[7]}{tires_width[8]}</b>\n\n'
                                         f'Цена: <u>{tires_width[11]}</u> рублей\n'
                                         f'Артикул: {tires_width[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Легковые шины\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {tires_width[2]}\n'
                                         f'🚘 Модель: {tires_width[3]}\n'
                                         f'🚘 Ширина и высота: {tires_width[4]}/{tires_width[5]}\n'
                                         f'🚘 Диаметр в дюймах: {tires_width[6]}\n'
                                         f'🚘 Индекс нагрузки и скорости: {tires_width[7]}{tires_width[8]}\n'
                                         f'🚘 Время года: {tires_width[9]}\n'
                                         f'🚘 Run Flat: Нет\n'
                                         f'🚘 Остаток протектора: {tires_width[10]} мм.\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()

async def pick_up_product_tires_height(message: types.Message) -> None:
    all_height_tires = cur.execute('SELECT height FROM tires').fetchall()
    kb_height_tires = types.InlineKeyboardMarkup(row_width=2)
    for height in range(len(all_height_tires)):
        one_height_tires = all_height_tires[height][0]
        kb_height_tires.add(types.InlineKeyboardButton(text=f'{one_height_tires}',
                                                       callback_data=cb_pick_up.new(msg_pick_up=f'{one_height_tires}')))
    await ProductSelection.tires_height.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_height_tires,
                           parse_mode='HTML')

async def send_pick_up_product_tires_height(callback_query: types.CallbackQuery,
                                            callback_data: dict,
                                            state: FSMContext) -> None:
    async with state.proxy():
        height = callback_data['msg_pick_up']
        send_all_tires_height = cur.execute(
            'SELECT * from tires WHERE height == "{height}"'.format(height=height)
        ).fetchall()
        for tires_height in send_all_tires_height:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=tires_height[1],
                                 caption=f'<b>{tires_height[2]} {tires_height[3]} '
                                         f'{tires_height[4]}/{tires_height[5]} D{tires_height[6]} '
                                         f'{tires_height[7]}{tires_height[8]}</b>\n\n'
                                         f'Цена: <u>{tires_height[11]}</u> рублей\n'
                                         f'Артикул: {tires_height[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Легковые шины\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {tires_height[2]}\n'
                                         f'🚘 Модель: {tires_height[3]}\n'
                                         f'🚘 Ширина и высота: {tires_height[4]}/{tires_height[5]}\n'
                                         f'🚘 Диаметр в дюймах: {tires_height[6]}\n'
                                         f'🚘 Индекс нагрузки и скорости: {tires_height[7]}{tires_height[8]}\n'
                                         f'🚘 Время года: {tires_height[9]}\n'
                                         f'🚘 Run Flat: Нет\n'
                                         f'🚘 Остаток протектора: {tires_height[10]} мм.\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()

async def pick_up_product_tires_diameter(message: types.Message) -> None:
    all_diameter_tires = cur.execute('SELECT diameter FROM tires').fetchall()
    kb_diameter_tires = types.InlineKeyboardMarkup(row_width=2)
    for diameter in range(len(all_diameter_tires)):
        one_diameter_tires = all_diameter_tires[diameter][0]
        kb_diameter_tires.add(types.InlineKeyboardButton(text=f'{one_diameter_tires}',
                                                         callback_data=cb_pick_up.new(msg_pick_up=f'{one_diameter_tires}')))

    await ProductSelection.tires_diameter.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_diameter_tires,
                           parse_mode='HTML')

async def send_pick_up_product_tires_diameter(callback_query: types.CallbackQuery,
                                              callback_data: dict,
                                              state: FSMContext) -> None:
    async with state.proxy():
        diameter = callback_data['msg_pick_up']
        send_all_tires_diameter = cur.execute(
            'SELECT * from tires WHERE diameter == "{diameter}"'.format(diameter=diameter)
        ).fetchall()
        for tires_diameter in send_all_tires_diameter:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=tires_diameter[1],
                                 caption=f'<b>{tires_diameter[2]} {tires_diameter[3]} '
                                         f'{tires_diameter[4]}/{tires_diameter[5]} D{tires_diameter[6]} '
                                         f'{tires_diameter[7]}{tires_diameter[8]}</b>\n\n'
                                         f'Цена: <u>{tires_diameter[11]}</u> рублей\n'
                                         f'Артикул: {tires_diameter[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Легковые шины\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {tires_diameter[2]}\n'
                                         f'🚘 Модель: {tires_diameter[3]}\n'
                                         f'🚘 Ширина и высота: {tires_diameter[4]}/{tires_diameter[5]}\n'
                                         f'🚘 Диаметр в дюймах: {tires_diameter[6]}\n'
                                         f'🚘 Индекс нагрузки и скорости: {tires_diameter[7]}{tires_diameter[8]}\n'
                                         f'🚘 Время года: {tires_diameter[9]}\n'
                                         f'🚘 Run Flat: Нет\n'
                                         f'🚘 Остаток протектора: {tires_diameter[10]} мм.\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()

async def pick_up_product_wheels(message: types.Message) -> None:
    if len(all_articles_wheels) == 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<i>Упссс... А данный вид товаров закончился...\n\n'
                                    f'Прости, но я не могу тебе пока ничего предложить.\n'
                                    f'Могу я помочь чем-нибудь ещё?</i>',
                               reply_markup=kb_menu,
                               parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Я понял тебя\n'
                                    'Теперь выбери по какому параметру тебе важно найти свой товар '
                                    'и я тебе следующим сообщением вышлю их варианты.</i>',
                               reply_markup=kb_wheels_parameters,
                               parse_mode='HTML')

async def pick_up_product_wheels_rim_width(message: types.Message) -> None:
    all_rim_width_wheels = cur.execute('SELECT rim_width FROM wheels').fetchall()
    kb_rim_width_wheels = types.InlineKeyboardMarkup(row_width=2)
    for rim_width in range(len(all_rim_width_wheels)):
        one_rim_width_wheels = all_rim_width_wheels[rim_width][0]
        kb_rim_width_wheels.add(types.InlineKeyboardButton(text=f'{one_rim_width_wheels}',
                                                           callback_data=cb_pick_up.new(
                                                               msg_pick_up=f'{one_rim_width_wheels}')))
    await ProductSelection.wheels_rim_width.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_rim_width_wheels,
                           parse_mode='HTML')

async def send_pick_up_product_wheels_rim_width(callback_query: types.CallbackQuery,
                                                callback_data: dict,
                                                state: FSMContext) -> None:
    async with state.proxy():
        rim_width = callback_data['msg_pick_up']
        send_all_wheels_rim_width = cur.execute(
            'SELECT * from wheels WHERE rim_width == "{rim_width}"'.format(rim_width=rim_width)
        ).fetchall()
        for wheels_rim_width in send_all_wheels_rim_width:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=wheels_rim_width[1],
                                 caption=f'<b>{wheels_rim_width[2]} {wheels_rim_width[3]} '
                                         f'D{wheels_rim_width[5]} {wheels_rim_width[7]}x'
                                         f'{wheels_rim_width[8]}</b>\n\n'
                                         f'Цена: <u>{wheels_rim_width[10]}</u> рублей\n'
                                         f'Артикул: {wheels_rim_width[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Диски\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {wheels_rim_width[2]}\n'
                                         f'🚘 Модель: {wheels_rim_width[3]}\n'
                                         f'🚘 Ширина оборота в дюймах: {wheels_rim_width[4]}\n'
                                         f'🚘 Диаметр в дюймах: {wheels_rim_width[5]}\n'
                                         f'🚘 Вылет (ET): {wheels_rim_width[6]}\n'
                                         f'🚘 Количество отверстий: {wheels_rim_width[7]}\n'
                                         f'🚘 Диаметр расположения отверстий: {wheels_rim_width[8]}\n'
                                         f'🚘 Центральное отверстие (DIA): {wheels_rim_width[9]}\n'
                                         f'🚘 Тип диска: Литые\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()

async def pick_up_product_wheels_diameter(message: types.Message) -> None:
    all_diameter_wheels = cur.execute('SELECT diameter FROM wheels').fetchall()
    kb_diameter_wheels = types.InlineKeyboardMarkup(row_width=2)
    for diameter in range(len(all_diameter_wheels)):
        one_diameter_wheels = all_diameter_wheels[diameter][0]
        kb_diameter_wheels.add(types.InlineKeyboardButton(text=f'{one_diameter_wheels}',
                                                          callback_data=cb_pick_up.new(
                                                              msg_pick_up=f'{one_diameter_wheels}')))
    await ProductSelection.wheels_diameter.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_diameter_wheels,
                           parse_mode='HTML')

async def send_pick_up_product_wheels_diameter(callback_query: types.CallbackQuery,
                                               callback_data: dict,
                                               state: FSMContext) -> None:
    async with state.proxy():
        diameter = callback_data['msg_pick_up']
        send_all_wheels_diameter = cur.execute(
            'SELECT * from wheels WHERE diameter == "{diameter}"'.format(diameter=diameter)
        ).fetchall()
        for wheels_diameter in send_all_wheels_diameter:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=wheels_diameter[1],
                                 caption=f'<b>{wheels_diameter[2]} {wheels_diameter[3]} '
                                         f'D{wheels_diameter[5]} {wheels_diameter[7]}x'
                                         f'{wheels_diameter[8]}</b>\n\n'
                                         f'Цена: <u>{wheels_diameter[10]}</u> рублей\n'
                                         f'Артикул: {wheels_diameter[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Диски\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {wheels_diameter[2]}\n'
                                         f'🚘 Модель: {wheels_diameter[3]}\n'
                                         f'🚘 Ширина оборота в дюймах: {wheels_diameter[4]}\n'
                                         f'🚘 Диаметр в дюймах: {wheels_diameter[5]}\n'
                                         f'🚘 Вылет (ET): {wheels_diameter[6]}\n'
                                         f'🚘 Количество отверстий: {wheels_diameter[7]}\n'
                                         f'🚘 Диаметр расположения отверстий: {wheels_diameter[8]}\n'
                                         f'🚘 Центральное отверстие (DIA): {wheels_diameter[9]}\n'
                                         f'🚘 Тип диска: Литые\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()

async def pick_up_product_wheels_departure(message: types.Message) -> None:
    all_departure_wheels = cur.execute('SELECT departure FROM wheels').fetchall()
    kb_departure_wheels = types.InlineKeyboardMarkup(row_width=2)
    for departure in range(len(all_departure_wheels)):
        one_departure_wheels = all_departure_wheels[departure][0]
        kb_departure_wheels.add(types.InlineKeyboardButton(text=f'{one_departure_wheels}',
                                                           callback_data=cb_pick_up.new(
                                                               msg_pick_up=f'{one_departure_wheels}')))
    await ProductSelection.wheels_departure.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вот! все данные, которые удалось найти в нашей базе.\n'
                                'Выбери то, что подходит именно тебе.'
                                'Я тут же вышлю полную информацию об этом товаре, '
                                'чтобы ты смог ознакомиться с товаром более детально.</i>',
                           reply_markup=kb_departure_wheels,
                           parse_mode='HTML')

async def send_pick_up_product_wheels_departure(callback_query: types.CallbackQuery,
                                                callback_data: dict,
                                                state: FSMContext) -> None:
    async with state.proxy():
        departure = callback_data['msg_pick_up']
        send_all_wheels_departure = cur.execute(
            'SELECT * from wheels WHERE departure == "{departure}"'.format(departure=departure)
        ).fetchall()
        for wheels_departure in send_all_wheels_departure:
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=wheels_departure[1],
                                 caption=f'<b>{wheels_departure[2]} {wheels_departure[3]} '
                                         f'D{wheels_departure[5]} {wheels_departure[7]}x'
                                         f'{wheels_departure[8]}</b>\n\n'
                                         f'Цена: <u>{wheels_departure[10]}</u> рублей\n'
                                         f'Артикул: {wheels_departure[0]}\n\n'
                                         f'<b>Характеристики</b>\n\n'
                                         f'🚘 Тип товара: Диски\n'
                                         f'🚘 Состояние: Б/у\n'
                                         f'🚘 Производитель: {wheels_departure[2]}\n'
                                         f'🚘 Модель: {wheels_departure[3]}\n'
                                         f'🚘 Ширина оборота в дюймах: {wheels_departure[4]}\n'
                                         f'🚘 Диаметр в дюймах: {wheels_departure[5]}\n'
                                         f'🚘 Вылет (ET): {wheels_departure[6]}\n'
                                         f'🚘 Количество отверстий: {wheels_departure[7]}\n'
                                         f'🚘 Диаметр расположения отверстий: {wheels_departure[8]}\n'
                                         f'🚘 Центральное отверстие (DIA): {wheels_departure[9]}\n'
                                         f'🚘 Тип диска: Литые\n\n',
                                 reply_markup=kb_menu,
                                 parse_mode='HTML')
    await state.finish()



def register_handlers_dialogue_others_pick_up_pr(dp: Dispatcher) -> None:
    dp.register_message_handler(pick_up_product,
                                Text(equals='Хочу подобрать товар!',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(pick_up_product_tires,
                                Text(equals='По шинам',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(pick_up_product_tires_width,
                                Text(equals='Ширина',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_tires_width,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.tires_width)
    dp.register_message_handler(pick_up_product_tires_height,
                                Text(equals='Высота',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_tires_height,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.tires_height)
    dp.register_message_handler(pick_up_product_tires_diameter,
                                Text(equals='Диаметр шины',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_tires_diameter,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.tires_diameter)
    dp.register_message_handler(pick_up_product_wheels,
                                Text(equals='По дискам',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(pick_up_product_wheels_rim_width,
                                Text(equals='Ширина обода',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_wheels_rim_width,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.wheels_rim_width)
    dp.register_message_handler(pick_up_product_wheels_diameter,
                                Text(equals='Диаметр колеса',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_wheels_diameter,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.wheels_diameter)
    dp.register_message_handler(pick_up_product_wheels_departure,
                                Text(equals='Вылет или ET',
                                     ignore_case=True),
                                state=None)
    dp.register_callback_query_handler(send_pick_up_product_wheels_departure,
                                       cb_pick_up.filter(),
                                       state=ProductSelection.wheels_departure)
