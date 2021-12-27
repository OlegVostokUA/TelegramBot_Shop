from aiogram.utils import executor
from create_bot import dp
from database import sqlite_db

async def on_startup(__):
    print('BOT online')
    sqlite_db.sql_start()
    sqlite_db.sql_cl_start()

from handlers import client, admin, others

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
others.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)