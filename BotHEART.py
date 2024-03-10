from aiogram import executor
from createbot import *
from data_base import sqlite_db
from handlers import filters, commands, ButKb


async def on_startup(d):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

ButKb.register_handlers_buttons(dp)
filters.register_handlers_filters(dp)
commands.register_handlers_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)