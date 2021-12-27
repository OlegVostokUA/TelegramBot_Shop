from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters import Text
from database import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    descr = State()
    price = State()

ID = None

# @dp.message_handler(commands=['moder'], is_chat_admin = True)
async def make_changes_cmd(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Hello Boss!', reply_markup=admin_kb.button_case_admin)
    await message.delete()

# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id ==ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название')

# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')

# @dp.message_handler(state=FSMAdmin.descr)
async def load_descr(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['descr'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи цену')

# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()

# @dp.callback_query_handler(Text(startswith=('del ')))
async def del_callback_run(callback_querry: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_querry.data.replace('del ', ''))
    await callback_querry.answer(text=f'{callback_querry.data.replace("del ", "")} удалена.', show_alert=True)

# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))

# @dp.callback_query_handler(Text(startswith=('del ')))
async def del_order_callback_run(callback_order_querry: types.CallbackQuery):
    await sqlite_db.sql_cl_delete_command(callback_order_querry.data.replace('odrdel ', ''))
    await callback_order_querry.answer(text=f'{callback_order_querry.data.replace("odrdel ", "")} удалена.', show_alert=True)

# @dp.message_handler(commands='Удалить_заказ')
async def delete_order_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_cl_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'Имя: {ret[0]}\nЗаказ: {ret[1]}\nАдрес: {ret[2]}'
                                                         f'\nТелефон: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить_заказ {ret[0]}', callback_data=f'odrdel {ret[0]}')))

# @dp.message_handler(commands='Заказы')
async def orders_command(message: types.Message):
    if message.from_user.id == ID:
        await sqlite_db.sql_cl_read(message)

# @dp.message_handler(state='*', commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_cmd(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_descr, state=FSMAdmin.descr)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_cmd, state='*', commands='отмена')
    dp.register_message_handler(cancel_cmd, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_cmd, commands=['moder'], is_chat_admin = True)
    dp.register_callback_query_handler(del_callback_run, Text(startswith=('del ')))
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_message_handler(orders_command, commands='Заказы')
    dp.register_callback_query_handler(del_order_callback_run, Text(startswith=('odrdel ')))
    dp.register_message_handler(delete_order_item, commands='Удалить_заказ')


