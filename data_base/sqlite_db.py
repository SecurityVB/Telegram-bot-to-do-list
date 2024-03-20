import sqlite3 as sq
from createbot import *
from KeyBoards.keyboards import *
import datetime

class DB_SYMBOLS:
    DB_TASK_DONE = '-~*&1*~-'
    DB_TASK_NOTDONE = '-~*&0*~-'
    DB_LIST_PROBEL = '-~*&*~-'


def sql_start():
    global base, cur

    base = sq.connect('TABLE_TODOLIST.db')
    cur = base.cursor()
    if base:
        print('data base connected')
    
    base.execute('CREATE TABLE IF NOT EXISTS ToDoList(user_id BINDING PRIMARY KEY, register_date DATETIME, spisok TEXT, tasks BINDING, completed_tasks BINDING)') 
    base.commit()


async def sql_add_id(message):
    id_user = message.from_user.id
    if (id_user,) not in cur.execute('SELECT user_id FROM ToDOList').fetchall():
        base.execute('INSERT INTO ToDoList (user_id) VALUES (?)', (id_user,))
        base.commit()
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        base.execute('UPDATE ToDoList SET register_date = (?)', (current_timestamp,))
        base.commit()


async def sql_add_proverka(message):
    id_user = message.from_user.id

    DB_TODOLIST = cur.execute('SELECT spisok FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
    for i in DB_TODOLIST:
        DB_TODOLIST = i

    if DB_TODOLIST != None:

        tasks = DB_TODOLIST.split(DB_SYMBOLS.DB_LIST_PROBEL)
        show_tasks = ''

        while '' in tasks:
            tasks.remove('')

        for i in tasks:

            if i != '' and DB_SYMBOLS.DB_TASK_NOTDONE in i:
                task_notdone = i.replace(DB_SYMBOLS.DB_TASK_NOTDONE, '')
                show_tasks += f'<b>{tasks.index(i) + 1})</b> {task_notdone}\n'

            if i != '' and DB_SYMBOLS.DB_TASK_DONE in i:
                task_done = i.replace(DB_SYMBOLS.DB_TASK_DONE, '')
                show_tasks += f'<b>{tasks.index(i) + 1})</b> <s>{task_done}</s>\n'

        del_msg = await message.answer('...', reply_markup = types.ReplyKeyboardRemove())
        await del_msg.delete()
        await bot.send_message(message.chat.id, text = show_tasks, reply_markup = func_kb, parse_mode = types.ParseMode.HTML)
    else:
        del_msg = await message.answer('...', reply_markup = types.ReplyKeyboardRemove())
        await del_msg.delete()
        await message.answer('У вас ещё нету задач. Добавьте их.', reply_markup = func_kb)


async def sql_show_tasks(message):
    id_user = message.from_user.id

    DB_TODOLIST = cur.execute('SELECT spisok FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
    for i in DB_TODOLIST:
        DB_TODOLIST = i

    if DB_TODOLIST != None:

        tasks = DB_TODOLIST.split(DB_SYMBOLS.DB_LIST_PROBEL)
        show_tasks = ''

        while '' in tasks:
            tasks.remove('')

        for i in tasks:

            if i != '' and DB_SYMBOLS.DB_TASK_NOTDONE in i:
                task_notdone = i.replace(DB_SYMBOLS.DB_TASK_NOTDONE, '')
                show_tasks += f'<b>{tasks.index(i) + 1})</b> {task_notdone}\n'

            if i != '' and DB_SYMBOLS.DB_TASK_DONE in i:
                task_done = i.replace(DB_SYMBOLS.DB_TASK_DONE, '')
                show_tasks += f'<b>{tasks.index(i) + 1})</b> <s>{task_done}</s>\n'

        await bot.send_message(message.chat.id, text = show_tasks, parse_mode = types.ParseMode.HTML)
    else:
        await message.answer('У вас ещё нету задач. Добавьте их.')


async def sql_add_task(message, add_task):
    id_user = message.from_user.id
    
    if 'SELECT' not in add_task:
        DB_TODOLIST = cur.execute('SELECT spisok FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
        for i in DB_TODOLIST:
            DB_TODOLIST = i
        if DB_TODOLIST == None:
            DB_TODOLIST = ''

        DB_TODOLIST += add_task + DB_SYMBOLS.DB_TASK_NOTDONE + DB_SYMBOLS.DB_LIST_PROBEL

        base.execute('UPDATE ToDoList SET spisok = (?) WHERE user_id = (?)', (DB_TODOLIST, id_user))
        base.commit()

        tasks_db = cur.execute('SELECT tasks FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
        for tasks in tasks_db:
            if tasks != None:
                tasks += 1
            else:
                tasks = 1
        
        base.execute('UPDATE ToDoList SET tasks = (?) WHERE user_id = (?)', (tasks, id_user))
        base.commit()

        await message.answer('Задача успешно добавлена.')
    else:
        await message.answer('Задача не может содержать "SELECT"')

    

async def sql_del_task(message, number):
    id_user = message.from_user.id

    if number == 'all':
        base.execute('UPDATE ToDoList SET spisok = (?) WHERE user_id = (?)', (None, id_user))
        base.commit()

    else:
        try:
            DB_TODOLIST = cur.execute('SELECT spisok FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
            for i in DB_TODOLIST:
                DB_TODOLIST = i

            DB_TODOLIST = DB_TODOLIST.split(DB_SYMBOLS.DB_LIST_PROBEL)
            while '' in DB_TODOLIST:
                DB_TODOLIST.remove('')

            number = number.split(' ')

            while '' in number:
                    number.remove('')

            for num in number:
                if num not in list("1234567890"):
                    for i in num:
                        if i not in list("1234567890"):
                            return await message.anwer('Ошибка.')

            if len(number) > 1:
                number_standart = number
                number = []

                for i in number_standart:
                    i = -((len(DB_TODOLIST) + 1) - int(i))
                    number.append(i)

                for index in number:
                    try:
                        DB_TODOLIST.pop(index)
                    except:
                        pass
            else:
                for index in number:
                    index = int(index) - 1
                    DB_TODOLIST.pop(index)


            DB_TODOLIST = DB_SYMBOLS.DB_LIST_PROBEL.join(DB_TODOLIST) + DB_SYMBOLS.DB_LIST_PROBEL

            base.execute('UPDATE ToDoList SET spisok = (?) WHERE user_id = (?)', (DB_TODOLIST, id_user))
            base.commit()
                
        except:
            await message.answer('Ошибка.')



async def sql_done_task(message, number):
    id_user = message.from_user.id

    try:
        DB_TODOLIST = cur.execute('SELECT spisok FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
        for i in DB_TODOLIST:
            DB_TODOLIST = i

        DB_TODOLIST = DB_TODOLIST.split(DB_SYMBOLS.DB_LIST_PROBEL)
        while '' in DB_TODOLIST:
            DB_TODOLIST.remove('')

        number = number.split(' ')

        while '' in number:
            number.remove('')

        for num in number:
            if num not in list("1234567890"):
                for i in num:
                    if i not in list("1234567890"):
                        return await message.anwer('Ошибка.')
            
        if len(number) > 1:
            number_standart = number
            number = []

            for i in number_standart:
                i = -((len(DB_TODOLIST) + 1) - int(i))
                number.append(i)

            for index in number:
                try:
                    DB_TODOLIST[index] = DB_TODOLIST[index].replace(DB_SYMBOLS.DB_TASK_NOTDONE, DB_SYMBOLS.DB_TASK_DONE)
                except:
                    pass
        else:
            for index in number:
                index = int(index) - 1
                DB_TODOLIST[index] = DB_TODOLIST[index].replace(DB_SYMBOLS.DB_TASK_NOTDONE, DB_SYMBOLS.DB_TASK_DONE)

        DB_TODOLIST = DB_SYMBOLS.DB_LIST_PROBEL.join(DB_TODOLIST) + DB_SYMBOLS.DB_LIST_PROBEL
        base.execute('UPDATE ToDoList SET spisok = (?) WHERE user_id = (?)', (DB_TODOLIST, id_user))
        base.commit()

        completed_tasks_db = cur.execute('SELECT completed_tasks FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
        for completed_tasks in completed_tasks_db:
            if completed_tasks != None:
                completed_tasks += 1
            else:
                completed_tasks = 1

        base.execute('UPDATE ToDOList SET completed_tasks = (?) WHERE user_id = (?)', (completed_tasks, id_user))
        base.commit()


    except:
        await message.answer('Ошибка.')



async def sql_statistics_tasks(message):
    id_user = message.from_user.id

    completed_tasks_db = cur.execute('SELECT completed_tasks FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
    for completed_tasks in completed_tasks_db:
        if completed_tasks != None:
            completed_tasks = completed_tasks

    tasks_db = cur.execute('SELECT tasks FROM ToDoList WHERE user_id = (?)', (id_user,)).fetchone()
    for tasks in tasks_db:
        if tasks != None:
            tasks = tasks

    try:
        ratio = (completed_tasks / tasks) * 100
        await message.answer(f"Всего выполненных задач: <b>{completed_tasks}</b>\nВсего было добавлено задач: <b>{tasks}</b>\nПродуктивность: <b>{ratio}%</b>", parse_mode = types.ParseMode.HTML)
    except:
        await message.answer(f"Всего выполненных задач: <b>{completed_tasks}</b>\nВсего было добавлено задач: <b>{tasks}</b>", parse_mode = types.ParseMode.HTML)