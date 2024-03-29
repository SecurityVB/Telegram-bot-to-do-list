import sqlite3 as sq
from createbot import *
from .hashing_task import *
from .db_support_functons import *
from KeyBoards.keyboards import *
import datetime



def sql_start():
    global base, cur

    base = sq.connect('DATE_BASE.db')
    cur = base.cursor()
    if base:
        print('data base connected')

    base.execute('CREATE TABLE IF NOT EXISTS TableToDo(user_id BINDING PRIMARY KEY, register_date DATETIME, spisok TEXT, total_tasks BINDING, completed_tasks BINDING)')
    base.commit()


async def sql_add_id(message):
    id_user = message.from_user.id
    if (id_user,) not in cur.execute('SELECT user_id FROM TableToDo').fetchall():
        base.execute('INSERT INTO TableToDo (user_id) VALUES (?)', (id_user,))
        base.commit()
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        base.execute('UPDATE TableToDo SET register_date = (?)', (current_timestamp,))
        base.commit()


async def sql_add_proverka(message):
    id_user = message.from_user.id

    spisok_from_db = cur.execute('SELECT spisok FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    spisok_tasks = Processing_the_to_do_list(spisok_from_db)

    if spisok_tasks: # Exists
        show_spisok_tasks = Preparing_spisok_tasks_for_display(spisok_tasks)

        del_msg = await message.answer('...', reply_markup=types.ReplyKeyboardRemove())
        await del_msg.delete()
        return await bot.send_message(message.chat.id, text=show_spisok_tasks, reply_markup=func_kb, parse_mode=types.ParseMode.HTML)

    else: # Does not exist
        del_msg = await message.answer('...', reply_markup=types.ReplyKeyboardRemove())
        await del_msg.delete()
        return await message.answer('У вас ещё нету задач. Добавьте их.', reply_markup=func_kb)

async def sql_show_tasks(message):
    id_user = message.from_user.id

    spisok_from_db = cur.execute('SELECT spisok FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    spisok_tasks = Processing_the_to_do_list(spisok_from_db)

    if spisok_tasks: # Exists
        show_spisok_tasks = Preparing_spisok_tasks_for_display(spisok_tasks)
        return await bot.send_message(message.chat.id, text=show_spisok_tasks, parse_mode=types.ParseMode.HTML)
    else: # Does not exist
        return await message.answer('У вас ещё нету задач. Добавьте их.')

async def sql_add_task(message, add_task):
    id_user = message.from_user.id

    add_task = hashing_(add_task, hasher)

    spisok_tasks_from_db = cur.execute('SELECT spisok FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    spisok_tasks = Checking_for_emptiness(spisok_tasks_from_db)

    spisok_tasks += add_task + DbSymbols.db_task_not_done + DbSymbols.task_space

    base.execute('UPDATE TableToDo SET spisok = (?) WHERE user_id = (?)', (spisok_tasks, id_user))
    base.commit()

    total_tasks_db = cur.execute('SELECT total_tasks FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    for total_tasks in total_tasks_db:
        if total_tasks:
            total_tasks += 1
        else:
            total_tasks = 1
        
    base.execute('UPDATE TableToDo SET total_tasks = (?) WHERE user_id = (?)', (total_tasks, id_user))
    base.commit()

    await message.answer('Задача успешно добавлена.')


async def sql_del_task(message, number):
    id_user = message.from_user.id

    if number == 'all':
        base.execute('UPDATE TableToDo SET spisok = (?) WHERE user_id = (?)', (None, id_user))
        base.commit()

    else:
        number = number.split()
        try:
            spisok_from_db = cur.execute('SELECT spisok FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
            spisok_tasks = Processing_the_to_do_list(spisok_from_db)

            if checking_task_selector(number):
                if len(number) > 1:
                    number_standart = number
                    number = []

                    for i in number_standart:
                        i = -((len(spisok_tasks) + 1) - int(i))
                        number.append(i)

                    for index in number:
                        try:
                            spisok_tasks.pop(index)
                        except:
                            pass
                else:
                    for index in number:
                        index = int(index) - 1
                        spisok_tasks.pop(index)


                spisok_tasks = DbSymbols.task_space.join(spisok_tasks) + DbSymbols.task_space

                base.execute('UPDATE TableToDo SET spisok = (?) WHERE user_id = (?)', (spisok_tasks, id_user))
                base.commit()
            else:
                await message.answer('Ошибка.')


                
        except:
            await message.answer('Ошибка.')


async def sql_done_task(message, number):
    id_user = message.from_user.id

    number = number.split()

    try:
        spisok_from_db = cur.execute('SELECT spisok FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
        spisok_tasks = Processing_the_to_do_list(spisok_from_db)

        if checking_task_selector(number):
            if len(number) > 1:
                number_standart = number
                number = []

                for i in number_standart:
                    i = -((len(spisok_tasks) + 1) - int(i))
                    number.append(i)

                for index in number:
                    try:
                        spisok_tasks[index] = spisok_tasks[index].replace(DbSymbols.db_task_not_done, DbSymbols.db_task_done)
                    except:
                        pass
            else:
                for index in number:
                    index = int(index) - 1
                    spisok_tasks[index] = spisok_tasks[index].replace(DbSymbols.db_task_not_done, DbSymbols.db_task_done)

            spisok_tasks = DbSymbols.task_space.join(spisok_tasks) + DbSymbols.task_space
            base.execute('UPDATE TableToDo SET spisok = (?) WHERE user_id = (?)', (spisok_tasks, id_user))
            base.commit()

            completed_tasks = cur.execute('SELECT completed_tasks FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
            completed_tasks = Checking_for_emptiness(completed_tasks)
            if completed_tasks:
                completed_tasks += 1
            else:
                completed_tasks = 1

            base.execute('UPDATE TableToDo SET completed_tasks = (?) WHERE user_id = (?)', (completed_tasks, id_user))
            base.commit()

        else:
            await message.answer('Ошибка.')

    except:
        await message.answer('Ошибка.')


async def sql_statistics_tasks(message):
    id_user = message.from_user.id

    completed_tasks_db = cur.execute('SELECT completed_tasks FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    completed_tasks = Checking_for_emptiness(completed_tasks_db)
    if completed_tasks:
        completed_tasks = completed_tasks
    else:
        completed_tasks = 0

    total_tasks_db = cur.execute('SELECT total_tasks FROM TableToDo WHERE user_id = (?)', (id_user,)).fetchone()
    total_tasks = Checking_for_emptiness(total_tasks_db)
    if total_tasks:
        total_tasks = total_tasks
    else:
        total_tasks = 0

    try:
        ratio = round((completed_tasks / total_tasks) * 100)
        await message.answer(f"Всего выполненных задач: {completed_tasks}\nВсего было добавлено задач: {total_tasks}\nПродуктивность: {ratio}%")
    except:
        await message.answer(f"Всего выполненных задач: {completed_tasks}\nВсего было добавлено задач: {total_tasks}")