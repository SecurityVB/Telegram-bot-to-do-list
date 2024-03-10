from aiogram import types, filters, Dispatcher

from createbot import *
from KeyBoards import *

#@dp.message_handler(filters.Text(contains='Привет'))
async def msg_handler(message: types.Message):
    await message.answer('Привет')
    


def register_handlers_filters(dp: Dispatcher):
    dp.register_message_handler(msg_handler, filters.Text(equals = 'Привет'))
