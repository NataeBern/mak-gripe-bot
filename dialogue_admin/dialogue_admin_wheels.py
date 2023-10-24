from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Python.Mak_Gripe_bot.auxiliary_files.config import token_API, ADMIN, chanel_URL, chanel_ID, bot_URL
from Python.Mak_Gripe_bot.keyboards.kb import kb_cancel_admin, kb_menu_admin
from Python.Mak_Gripe_bot.sql.sqlite import random_article, create_wheels, edit_wheels

import sqlite3



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)



class NewPostWheels(StatesGroup):
    photo = State()
    manufacturer = State()
    model = State()
    rim_width = State()
    diameter = State()
    departure = State()
    number_of_holes = State()
    diameter_hole = State()
    central_hole = State()
    price = State()
    number_of_sets = State()



async def create_post_wheels(message: types.Message) -> None:
    await NewPostWheels.photo.set()
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Принято!\n\n'
                                f'Отправь мне фотографию товара, '
                                f'которую ты хочешь увидеть больше всего в данном посте.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await create_wheels(random_article=random_article)

async def check_photo_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Это не фотография!\n'
                                f'Попробуй ещё раз!</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_photo_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['photo'] = message.photo[2].file_id
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Отличный выбор!\n'
                                f'А сейчас расскажи мне о производителе этих колёс.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def save_manufacturer_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['manufacturer'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Что ж... Назови мне модель данного товара.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def save_model_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['model'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай теперь поговорим о параметрах.\n'
                                f'Какова ширина обода колеса? Укажи значение в дюймах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_rim_width_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальная ширина обода колеса\n\n'
                                f'Давай попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_rim_width_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['rim_width'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>А диаметр какой?\n'
                                f'Напиши мне его в дюймах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_diameter_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальный диаметр!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_diameter_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['diameter'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>А что касаемо вылета колеса или ЕТ?\n'
                                f'Какое тут значение?</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_departure_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальное значение вылета!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_departure_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['departure'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Мне кажется, что также важно указать количество отверстий в колесе... '
                                f'Или нет? 😏</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_number_of_holes_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не количество отверстий для колеса!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_number_of_holes_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['number_of_holes'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Теперь пора указать диаметр расположения отверстий.\n'
                                f'Напиши примерное значение с точностью до десятых долей.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_diameter_hole_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальный диаметр отверстий колеса!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_diameter_hole_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['diameter_hole'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Ура! Осталось совсем немного!\n'
                                f'Раз мы указали диаметр расположения отверстий в колесе, то '
                                f'давай также укажем и центральное отверстие или DIA.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_central_hole_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальное значение для DIA!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_central_hole_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['central_hole'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Теперь укажи мне цену за один комплект колёс.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_price_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или слишком высокая цена!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_price_wheels(message: types.Message, state: FSMContext):
    async with state.proxy() as data_wheels:
        data_wheels['price'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>И последнее!\n\n'
                                f'Давай занесём в нашу базу сколько всего будет этих комплектов, '
                                f'чтобы я мог отследить его и уменьшать количество, '
                                f'когда товар будет продан или забронирован.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostWheels.next()

async def check_number_of_sets_wheels(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Ты указываешь мне не число!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_number_of_sets_wheels(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_wheels:
        data_wheels['number_of_sets'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Наконец-то! Я и сам уже подустал...\n\n'
                                f'Твои данные сохранены и отобразились в новом посте на твоём Telegram-канале - '
                                f'<a href="{chanel_URL}">MakGripe | МакГрайп</a></i>',
                           reply_markup=kb_menu_admin,
                           parse_mode='HTML')
    async with state.proxy() as data_wheels:
        msg = await bot.send_photo(chat_id=chanel_ID,
                                   photo=data_wheels['photo'],
                                   caption=f'<b>{data_wheels["manufacturer"]} {data_wheels["model"]} '
                                           f'D{data_wheels["diameter"]} {data_wheels["number_of_holes"]}x'
                                           f'{data_wheels["diameter_hole"]}</b>\n\n'
                                           f'Цена: <u>{data_wheels["price"]}</u> рублей\n'
                                           f'Артикул: {random_article}\n\n'
                                           f'<b>Характеристики</b>\n\n'
                                           f'🚘 Тип товара: Диски\n'
                                           f'🚘 Состояние: Б/у\n'
                                           f'🚘 Производитель: {data_wheels["manufacturer"]}\n'
                                           f'🚘 Модель: {data_wheels["model"]}\n'
                                           f'🚘 Ширина оборота в дюймах: {data_wheels["rim_width"]}\n'
                                           f'🚘 Диаметр в дюймах: {data_wheels["diameter"]}\n'
                                           f'🚘 Вылет (ET): {data_wheels["departure"]}\n'
                                           f'🚘 Количество отверстий: {data_wheels["number_of_holes"]}\n'
                                           f'🚘 Диаметр расположения отверстий: {data_wheels["diameter_hole"]}\n'
                                           f'🚘 Центральное отверстие (DIA): {data_wheels["central_hole"]}\n'
                                           f'🚘 Тип диска: Литые\n\n'
                                           f'Если хочешь купить именно этот товар, то переходи по ссылке, '
                                           f'написав нашему Telegram-боту - <a href="{bot_URL}">Mak_Gripe_bot</a>',
                                   parse_mode='HTML')
        con = sqlite3.connect('C:\\Users\\nastm\\OneDrive\\Рабочий стол\\Python\\Mak_Gripe_bot\\sql\\database.db')
        with con:
            cur = con.cursor()
            cur.execute(
                'UPDATE wheels SET msg_chanel_id = "{msg_chanel_id}" WHERE article == "{article}"'.format(
                    msg_chanel_id=msg.message_id,
                    article=random_article
                )
            )

    await edit_wheels(state=state, random_article=random_article)
    await state.finish()



def register_handlers_dialogue_admin_wheels(dp: Dispatcher) -> None:
    dp.register_message_handler(create_post_wheels,
                                Text(equals='Литые диски',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(check_photo_wheels,
                                lambda message: not message.photo,
                                state=NewPostWheels.photo)
    dp.register_message_handler(save_photo_wheels,
                                content_types=['photo'],
                                state=NewPostWheels.photo)
    dp.register_message_handler(save_manufacturer_wheels,
                                state=NewPostWheels.manufacturer)
    dp.register_message_handler(save_model_wheels,
                                state=NewPostWheels.model)
    dp.register_message_handler(check_rim_width_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 10,
                                state=NewPostWheels.rim_width)
    dp.register_message_handler(save_rim_width_wheels,
                                state=NewPostWheels.rim_width)
    dp.register_message_handler(check_diameter_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 100,
                                state=NewPostWheels.diameter)
    dp.register_message_handler(save_diameter_wheels,
                                state=NewPostWheels.diameter)
    dp.register_message_handler(check_departure_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 100,
                                state=NewPostWheels.departure)
    dp.register_message_handler(save_departure_wheels,
                                state=NewPostWheels.departure)
    dp.register_message_handler(check_number_of_holes_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 10,
                                state=NewPostWheels.number_of_holes)
    dp.register_message_handler(save_number_of_holes_wheels,
                                state=NewPostWheels.number_of_holes)
    dp.register_message_handler(check_diameter_hole_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 1000,
                                state=NewPostWheels.diameter_hole)
    dp.register_message_handler(save_diameter_hole_wheels,
                                state=NewPostWheels.diameter_hole)
    dp.register_message_handler(check_central_hole_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 100,
                                state=NewPostWheels.central_hole)
    dp.register_message_handler(save_central_hole_wheels,
                                state=NewPostWheels.central_hole)
    dp.register_message_handler(check_price_wheels,
                                lambda message: not message.text.isdigit() or float(message.text) > 100000,
                                state=NewPostWheels.price)
    dp.register_message_handler(save_price_wheels,
                                state=NewPostWheels.price)
    dp.register_message_handler(check_number_of_sets_wheels,
                                lambda message: not message.text.isdigit(),
                                state=NewPostWheels.number_of_sets)
    dp.register_message_handler(save_number_of_sets_wheels,
                                state=NewPostWheels.number_of_sets)