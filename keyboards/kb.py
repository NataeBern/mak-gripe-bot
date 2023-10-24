from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from Python.Mak_Gripe_bot.auxiliary_files.config import chanel_URL



cb = CallbackData('action', 'msg_text')
cb_pick_up = CallbackData('action_pick_up', 'msg_pick_up')



btn_user_subcribed = InlineKeyboardButton(text='Перейти подписаться', url=chanel_URL)
btn_user_isnt_subcribed = InlineKeyboardButton(text='Уже подписан', callback_data='userisntsubcribed')
menu_subcride = InlineKeyboardMarkup(row_width=2).add(btn_user_subcribed).insert(btn_user_isnt_subcribed)



kb_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
bt_creating_post = KeyboardButton(text='Создать новый пост')
bt_all_applications = KeyboardButton(text='Посмотреть все заявки')
kb_menu_admin.add(bt_creating_post, bt_all_applications)

kb_cancel_admin = ReplyKeyboardMarkup(resize_keyboard=True)
bt_cancel_admin = KeyboardButton(text='Отменить')
kb_cancel_admin.add(bt_cancel_admin)

kb_products = ReplyKeyboardMarkup(resize_keyboard=True)
bt_tires = KeyboardButton(text='Легковые шины')
bt_wheels = KeyboardButton(text='Литые диски')
kb_products.add(bt_tires).insert(bt_wheels)

kb_speed = InlineKeyboardMarkup(row_width=2)
bt_T = InlineKeyboardButton(text='T',
                                  callback_data='speed_T')
bt_H = InlineKeyboardButton(text='H',
                                  callback_data='speed_H')
bt_R = InlineKeyboardButton(text='R',
                                  callback_data='speed_R')
bt_V = InlineKeyboardButton(text='V',
                                  callback_data='speed_V')
kb_speed.add(bt_T, bt_H).add(bt_R, bt_V)

kb_season = InlineKeyboardMarkup(row_width=2)
bt_winter_studded = InlineKeyboardButton(text='Зимние шипованные',
                                         callback_data='winter_studded')
bt_winter_non_studded = InlineKeyboardButton(text='Зимние нешипованные',
                                             callback_data='winter_non_studded')
bt_summer = InlineKeyboardButton(text='Летние',
                                 callback_data='summer')
bt_all_season = InlineKeyboardButton(text='Всесезонные',
                                     callback_data='all_season')
kb_season.add(bt_winter_studded, bt_winter_non_studded).add(bt_summer, bt_all_season)



kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
bt_buy_product = KeyboardButton(text='Хочу купить товар!')
bt_puck_up_product = KeyboardButton(text='Хочу подобрать товар!')
kb_menu.add(bt_buy_product, bt_puck_up_product)

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
bt_cancel = KeyboardButton(text='В начало меню')
kb_cancel.add(bt_cancel)

kb_application = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
kb_application.add(KeyboardButton(text='Да, давай!'))

kb_type_product = InlineKeyboardMarkup(row_width=2)
bt_type_tires = InlineKeyboardButton(text='Легковые шины',
                                     callback_data='passenger_tires')
bt_type_wheels = InlineKeyboardButton(text='Литые диски',
                                      callback_data='cast_wheels')
kb_type_product.add(bt_type_tires, bt_type_wheels)

kb_products_pick_up = ReplyKeyboardMarkup(resize_keyboard=True)
bt_tires_pick_up = KeyboardButton(text='По шинам')
bt_wheels_pick_up = KeyboardButton(text='По дискам')
kb_products_pick_up.add(bt_tires_pick_up).insert(bt_wheels_pick_up)

kb_tire_parameters = ReplyKeyboardMarkup(resize_keyboard=True)
bt_width_tires = KeyboardButton(text='Ширина')
bt_height_tires = KeyboardButton(text='Высота')
bt_diameter_tire = KeyboardButton(text='Диаметр шины')
kb_tire_parameters.add(bt_width_tires).add(bt_height_tires).insert(bt_diameter_tire)

kb_wheels_parameters = ReplyKeyboardMarkup(resize_keyboard=True)
bt_rim_width_wheels = KeyboardButton(text='Ширина обода')
bt_diameter_wheels = KeyboardButton(text='Диаметр колеса')
bt_departure_wheels = KeyboardButton(text='Вылет или ET')
kb_wheels_parameters.add(bt_rim_width_wheels).add(bt_diameter_wheels).insert(bt_departure_wheels)