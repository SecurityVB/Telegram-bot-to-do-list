from .hashing_task import *


def Processing_the_to_do_list(spisok_from_db):
    for i in spisok_from_db:
        if i != None:
            spisok_from_db = rehashing_(i, hasher)

            spisok_tasks = spisok_from_db.split(DbSymbols.task_space)
            while '' in spisok_tasks:
                spisok_tasks.remove('')

        else:
            return False

    return spisok_tasks


def Preparing_spisok_tasks_for_display(spisok_tasks):
    show_spisok_tasks = ''
    for task in spisok_tasks:
        if DbSymbols.db_task_not_done in task:
            task_not_done = task.replace(DbSymbols.db_task_not_done, '')
            show_spisok_tasks += f'<b>{spisok_tasks.index(task) + 1})</b> {task_not_done}\n'

        elif DbSymbols.db_task_done in task:
            task_done = task.replace(DbSymbols.db_task_done, '')
            show_spisok_tasks += f'<b>{spisok_tasks.index(task) + 1})</b> <s>{task_done}</s>\n'
    return show_spisok_tasks

def checking_task_selector(number):
    if isinstance(number, list):
        for num in number:
            try:
                num = int(num)
                if num < 0:
                    return False
                else:
                    return True
            except:
                return False
    elif isinstance(number, int):
        try:
            number = int(number)
            if number < 0:
                return False
            else:
                return True
        except:
            return False
    else:
        return False

def Checking_for_emptiness(db_element):
    for i in db_element:
        if i != None:
            return i
        else:
            return ''