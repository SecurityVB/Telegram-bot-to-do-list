from aiogram import Dispatcher,types

from data_base.sqlite_db import *
from createbot import *
from KeyBoards.keyboards import kb, integration_kb
# from data_base import sqlite_db


# @dp.message_handler(commands=['start'])
async def command_handler_start(message: types.Message):
    await sql_add_id(message)
    await message.answer('Что желаете?: ', reply_markup=kb)

'''***************************************************************************Команда ИНТЕГРАЦИИ*****************************************************************************************************'''

# @dp.message_handler(commands=['integrations'])
async def command_handler_int(message: types.Message):
    await bot.send_message(message.from_user.id, 'Интеграции:', reply_markup=integration_kb)
    await message.delete()



def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_handler_start, commands=['start'])
    dp.register_message_handler(command_handler_int, commands=['integrations'])