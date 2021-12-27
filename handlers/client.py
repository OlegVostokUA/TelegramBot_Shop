from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
from database import sqlite_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class FSMClient(StatesGroup):
    name_cl = State()
    goods = State()
    address = State()
    telephone = State()

# @dp.message_handler(commands='Заказать', State=None)
async def start_order(message: types.Message):
    await FSMClient.name_cl.set()
    await message.answer('Доброго времени суток. Как я могу к Вам обращатся?')

# @dp.message_handler(state=FSMClient.name_cl)
async def input_name_cl(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name_cl'] = message.text
    await FSMClient.next()
    await message.answer('Что бы Вы хотели заказать?')

# @dp.message_handler(state=FSMClient.goods)
async def input_goods(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['goods'] = message.text
    await FSMClient.next()
    await message.answer('Введите адрес для отправки заказа')

# @dp.message_handler(state=FSMClient.address)
async def input_address(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await FSMClient.next()
    await message.answer('Введите контактный телефон')

# @dp.message_handler(state=FSMClient.telephone)
async def input_telephone(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['telephone'] = message.text
    await sqlite_db.sql_cl_add_command(state)
    await state.finish()
    await message.answer('Спасибо. Ваша заявка добавлена в обработку. Мы с Вами свяжемся в течении суток')


# @dp.message_handler(commands=['start'])
async def command_start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Чего изволите?', reply_markup=kb_client)
    await message.delete()

# @dp.message_handler(commands=['help'])
async def command_help(message:types.Message):
    await bot.send_message(message.from_user.id, 'Хочешь что то? Бот в помощь))')
    await message.delete()

# @dp.message_handler(commands=['Режим_работы'])
async def command_shop_open(message: types.Message):
    await bot.send_message(message.from_user.id, '24/7/365')

# @dp.message_handler(commands=['Расположение'])
async def command_shop_place(message: types.Message):
    await bot.send_message(message.from_user.id, 'г. Киев')

# @dp.message_handler(commands=['Ассортимент'])
async def assort_command(message: types.Message):
    await sqlite_db.sql_read(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_shop_open, commands=['Режим_работы'])
    dp.register_message_handler(command_shop_place, commands=['Расположение'])
    dp.register_message_handler(assort_command, commands=['Ассортимент'])
    dp.register_message_handler(start_order, commands='Заказать', State=None)
    dp.register_message_handler(input_name_cl, state=FSMClient.name_cl)
    dp.register_message_handler(input_goods, state=FSMClient.goods)
    dp.register_message_handler(input_address, state=FSMClient.address)
    dp.register_message_handler(input_telephone, state=FSMClient.telephone)
