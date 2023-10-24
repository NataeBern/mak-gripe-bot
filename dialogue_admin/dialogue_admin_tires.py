from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Python.Mak_Gripe_bot.auxiliary_files.config import token_API, ADMIN, chanel_URL, chanel_ID, bot_URL
from Python.Mak_Gripe_bot.keyboards.kb import kb_menu_admin, kb_cancel_admin, kb_speed, kb_season
from Python.Mak_Gripe_bot.sql.sqlite import random_article, create_tires, edit_tires

import sqlite3



storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)



class NewPostTires(StatesGroup):
    photo = State()
    manufacturer = State()
    model = State()
    width = State()
    height = State()
    diameter = State()
    load = State()
    speed = State()
    season = State()
    remainder_tread = State()
    price = State()
    number_of_sets = State()



async def cancel_command_admin(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Как скажете!\n'
                                f'Чем ещё могу быть полезен?</i>',
                           reply_markup=kb_menu_admin,
                           parse_mode="HTML")
    await state.finish()

async def create_post_tires(message: types.Message) -> None:
    await NewPostTires.photo.set()
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Принято!\n\n'
                                f'Отправь мне фотографию товара, '
                                f'которую ты хочешь увидеть больше всего в данном посте.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await create_tires(random_article=random_article)

async def check_photo_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Это не фотография!\n'
                                f'Попробуй ещё раз!</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_photo_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['photo'] = message.photo[2].file_id
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Отличный выбор!\n'
                                f'А сейчас расскажи мне о производителе этих шин.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_manufacturer_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['manufacturer'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Что ж... Назови мне модель данного товара.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_model_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['model'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай теперь поговорим о параметрах?\n'
                                f'Какова ширина шины?</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_width_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальная ширина!\n\nДавай попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_width_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['width'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>А высота какая?</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_height_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальная длинна!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_height_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['height'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>А что касаемо диаметра?\n'
                                f'Напиши мне этот параметр в дюймах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_diameter_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальный диаметр!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_diameter_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['diameter'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>А индекс нагрузки?\n'
                                f'О нём важно знать будущим покупателям! Какой он?</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_load_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальный индекс нагрузки!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_load_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['load'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Мне кажется мы чуть не забыли про индекс скорости... 🤔\n\n'
                                f'Тогда выбери подходящий параметр, нажав на соответствующую кнопку.</i>',
                           reply_markup=kb_speed,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_t_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['speed'] = 'T'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай укажем на какой сезон рассчитаны эти шины?\n\n'
                                f'Как и в прошлый раз, ты должен выбрать подходящую категорию, '
                                f'кликнув на нужную кнопку.</i>',
                           reply_markup=kb_season,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_h_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['speed'] = 'H'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай укажем на какой сезон рассчитаны эти шины?\n\n'
                                f'Как и в прошлый раз, ты должен выбрать подходящую категорию, '
                                f'кликнув на нужную кнопку.</i>',
                           reply_markup=kb_season,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_r_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['speed'] = 'R'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай укажем на какой сезон рассчитаны эти шины?\n\n'
                                f'Как и в прошлый раз, ты должен выбрать подходящую категорию, '
                                f'кликнув на нужную кнопку.</i>',
                           reply_markup=kb_season,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_v_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['speed'] = 'V'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Давай укажем на какой сезон рассчитаны эти шины?\n\n'
                                f'Как и в прошлый раз, ты должен выбрать подходящую категорию, '
                                f'кликнув на нужную кнопку.</i>',
                           reply_markup=kb_season,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_winter_studded_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['season'] = 'Зимние шипованные'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Ура! Осталось совсем немного!\n'
                                f'Давай также укажем остаток протектора в миллиметрах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_winter_non_studded_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['season'] = 'Зимние нешипованные'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Ура! Осталось совсем немного!\n'
                                f'Давай также укажем остаток протектора в миллиметрах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_summer_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['season'] = 'Летние'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Ура! Осталось совсем немного!\n'
                                f'Давай также укажем остаток протектора в миллиметрах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def save_all_season_callback_handler_tires(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['season'] = 'Всесезонные'
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Ура! Осталось совсем немного!\n'
                                f'Давай также укажем остаток протектора в миллиметрах.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_remainder_tread_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или не реальное значение для остатка протектора!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_remainder_tread_tires(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['remainder_tread'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Теперь скажи мне цену за один комплект шин.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_price_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Это не число или слишком высокая цена!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_price_tires(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tires:
        data_tires['price'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>И последнее!\n\n'
                                f'Давай занесём в нашу базу сколько всего будет этих комплектов, '
                                f'чтобы я мог отследить его и уменьшать количество, '
                                f'когда товар будет продан или забронирован.</i>',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')
    await NewPostTires.next()

async def check_number_of_sets_tires(message: types.Message) -> None:
    await bot.send_message(chat_id=ADMIN,
                           text=f'Ты указываешь мне не число!\n\n'
                                f'Давай ты попробуешь снова?',
                           reply_markup=kb_cancel_admin,
                           parse_mode='HTML')

async def save_number_of_sets_tires(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data_tires:
        data_tires['number_of_sets'] = message.text
    await bot.send_message(chat_id=ADMIN,
                           text=f'<i>Наконец-то! Я и сам уже подустал...\n\n'
                                f'Твои данные сохранены и отобразились в новом посте на твоём Telegram-канале - '
                                f'<a href="{chanel_URL}">MakGripe | МакГрайп</a></i>',
                           reply_markup=kb_menu_admin,
                           parse_mode='HTML')
    async with state.proxy() as data_tires:
        msg = await bot.send_photo(chat_id=chanel_ID,
                                   photo=data_tires['photo'],
                                   caption=f'<b>{data_tires["manufacturer"]} {data_tires["model"]} '
                                           f'{data_tires["width"]}/{data_tires["height"]} D{data_tires["diameter"]} '
                                           f'{data_tires["load"]}{data_tires["speed"]}</b>\n\n'
                                           f'Цена: <u>{data_tires["price"]}</u> рублей\n'
                                           f'Артикул: {random_article}\n\n'
                                           f'<b>Характеристики</b>\n\n'
                                           f'🚘 Тип товара: Легковые шины\n'
                                           f'🚘 Состояние: Б/у\n'
                                           f'🚘 Производитель: {data_tires["manufacturer"]}\n'
                                           f'🚘 Модель: {data_tires["model"]}\n'
                                           f'🚘 Ширина и высота: {data_tires["width"]}/{data_tires["height"]}\n'
                                           f'🚘 Диаметр в дюймах: {data_tires["diameter"]}\n'
                                           f'🚘 Индекс нагрузки и скорости: {data_tires["load"]}{data_tires["speed"]}\n'
                                           f'🚘 Время года: {data_tires["season"]}\n'
                                           f'🚘 Run Flat: Нет\n'
                                           f'🚘 Остаток протектора: {data_tires["remainder_tread"]} мм.\n\n'
                                           f'Если хочешь купить именно этот товар, то переходи по ссылке, '
                                           f'написав нашему Telegram-боту - <a href="{bot_URL}">Mak_Gripe_bot</a>',
                                   parse_mode='HTML')
        con = sqlite3.connect('C:\\Users\\nastm\\OneDrive\\Рабочий стол\\Python\\Mak_Gripe_bot\\sql\\database.db')
        with con:
            cur = con.cursor()
            cur.execute(
                'UPDATE tires SET msg_chanel_id = "{msg_chanel_id}" WHERE article == "{article}"'.format(
                    msg_chanel_id=msg.message_id,
                    article=random_article
                )
            )
    await edit_tires(state=state, random_article=random_article)
    await state.finish()

def register_handlers_dialogue_admin_tires(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_command_admin,
                                Text(equals='Отменить',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(create_post_tires,
                                Text(equals='Легковые шины',
                                     ignore_case=True),
                                state=None)
    dp.register_message_handler(check_photo_tires,
                                lambda message: not message.photo,
                                state=NewPostTires.photo)
    dp.register_message_handler(save_photo_tires,
                                content_types=['photo'],
                                state=NewPostTires.photo)
    dp.register_message_handler(save_manufacturer_tires,
                                state=NewPostTires.manufacturer)
    dp.register_message_handler(save_model_tires,
                                state=NewPostTires.model)
    dp.register_message_handler(check_width_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 1000,
                                state=NewPostTires.width)
    dp.register_message_handler(save_width_tires,
                                state=NewPostTires.width)
    dp.register_message_handler(check_height_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 100,
                                state=NewPostTires.height)
    dp.register_message_handler(save_height_tires,
                                state=NewPostTires.height)
    dp.register_message_handler(check_diameter_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 100,
                                state=NewPostTires.diameter)
    dp.register_message_handler(save_diameter_tires,
                                state=NewPostTires.diameter)
    dp.register_message_handler(check_load_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 1000,
                                state=NewPostTires.load)
    dp.register_message_handler(save_load_tires,
                                state=NewPostTires.load)
    dp.register_callback_query_handler(save_t_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'speed_T',
                                       state=NewPostTires.speed)
    dp.register_callback_query_handler(save_h_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'speed_H',
                                       state=NewPostTires.speed)
    dp.register_callback_query_handler(save_r_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'speed_R',
                                       state=NewPostTires.speed)
    dp.register_callback_query_handler(save_v_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'speed_V',
                                       state=NewPostTires.speed)
    dp.register_callback_query_handler(save_winter_studded_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'winter_studded',
                                       state=NewPostTires.season)
    dp.register_callback_query_handler(save_winter_non_studded_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'winter_non_studded',
                                       state=NewPostTires.season)
    dp.register_callback_query_handler(save_summer_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'summer',
                                       state=NewPostTires.season)
    dp.register_callback_query_handler(save_all_season_callback_handler_tires,
                                       lambda callback_query: callback_query.data == 'all_season',
                                       state=NewPostTires.season)
    dp.register_message_handler(check_remainder_tread_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 1000,
                                state=NewPostTires.remainder_tread)
    dp.register_message_handler(save_remainder_tread_tires,
                                state=NewPostTires.remainder_tread)
    dp.register_message_handler(check_price_tires,
                                lambda message: not message.text.isdigit() or float(message.text) > 100000,
                                state=NewPostTires.price)
    dp.register_message_handler(save_price_tires,
                                state=NewPostTires.price)
    dp.register_message_handler(check_number_of_sets_tires,
                                lambda message: not message.text.isdigit(),
                                state=NewPostTires.number_of_sets)
    dp.register_message_handler(save_number_of_sets_tires,
                                state=NewPostTires.number_of_sets)