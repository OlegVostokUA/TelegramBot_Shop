from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('/Режим_работы')
button2 = KeyboardButton('/Расположение')
button3 = KeyboardButton('/Ассортимент')
button4 = KeyboardButton('/Заказать')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(button1).insert(button2).add(button3).insert(button4)
