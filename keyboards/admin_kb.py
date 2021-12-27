from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
button_orders = KeyboardButton('/Заказы')
button_delete_orders = KeyboardButton('/Удалить_заказ')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .insert(button_delete).add(button_orders).insert(button_delete_orders)
