from aiogram import types, filters, Dispatcher

from createbot import *
from KeyBoards.keyboards import *
from data_base.sqlite_db import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ParseMode

class FSMfucntional(StatesGroup):
    Add_Task_State = State()
    Del_Task_State = State()
    Done_Task_State = State()


#@dp.message_handler(filters.Text(equals='Список Дел'))
async def button_handler_list(message: types.Message):
    await sql_add_proverka(message)


#@dp.message_handler(filters.Text(equals='Статистика'))
async def button_handler_stat(message: types.Message):
    await completed_tasks(message)



@dp.message_handler(filters.Text(equals='Показать задачи'))
async def button_handler_ShowTask(message: types.Message):
    await sql_show_tasks(message)



#@dp.message_handler(filters.Text(equals='Добавить задачу'), state = None)
async def button_handler_AddTask(message: types.Message):
    await message.reply('Напишите задачу')
    await FSMfucntional.Add_Task_State.set()


#@dp.message_handler(state = FSMfucntional.Add_Task_State)
async def state_handler_Select(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Add_Task_State'] = message.text
    async with state.proxy() as data:
        add_task = data['Add_Task_State']

    await sql_add_task(message, add_task)
    
    await state.finish()


#@dp.message_handler(filters.Text(equals='Удалить задачу'))
async def button_handler_DelTask(message: types.Message):
    await message.reply('Напишите номера задач через пробел, которые хотите удалить. Чтобы удалить все задачи напишите <code>all</code>', parse_mode = types.ParseMode.HTML)
    await FSMfucntional.Del_Task_State.set()


# @dp.message_handler(state = FSMfucntional.Del_Task_State)
async def state_handler_DelTask(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Del_task_State'] = message.text
    async with state.proxy() as data:
        del_task = data['Del_task_State']

    await sql_del_task(message, del_task)
    
    await state.finish()

#@dp.message_handler(filters.Text(equals='Выполнил задачу'))
async def button_handler_DoneTask(message: types.Message):
    await message.reply('Напишите номера задач через пробел, которые уже выполнили')
    await FSMfucntional.Done_Task_State.set()


# @dp.message_handler(state = FSMfucntional.Done_Task_State)
async def state_handler_DoneTask(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Done_Task_State'] = message.text
    async with state.proxy() as data:
        del_task = data['Done_Task_State']

    await sql_done_task(message, del_task)
    
    await state.finish()


#@dp.message_handler(filters.Text(equals='Назад'))
async def button_handler_ShowTask(message: types.Message):
    del_msg = await message.answer('...', reply_markup = types.ReplyKeyboardRemove())
    await del_msg.delete()
    await message.answer('Что желаете?', reply_markup=kb)


def register_handlers_buttons(dp: Dispatcher):
    dp.register_message_handler(button_handler_list, filters.Text(equals='Список Дел'))
    dp.register_message_handler(button_handler_stat, filters.Text(equals='Статистика'))
    dp.register_message_handler(button_handler_ShowTask, filters.Text(equals='Показать задачи'))
    dp.register_message_handler(button_handler_AddTask, filters.Text(equals='Добавить задачу'), state = None)
    dp.register_message_handler(state_handler_Select, state = FSMfucntional.Add_Task_State)
    dp.register_message_handler(button_handler_DelTask, filters.Text(equals='Удалить задачу'))
    dp.register_message_handler(state_handler_DelTask, state = FSMfucntional.Del_Task_State)
    dp.register_message_handler(button_handler_DoneTask, filters.Text(equals='Выполнил задачу'))
    dp.register_message_handler(state_handler_DoneTask, state = FSMfucntional.Done_Task_State)
    dp.register_message_handler(button_handler_ShowTask, filters.Text(equals='Назад'))