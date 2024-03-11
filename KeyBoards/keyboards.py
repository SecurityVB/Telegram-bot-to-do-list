from aiogram import types



kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton(text='Список Дел'),
    types.KeyboardButton(text='Статистика')
]
kb.add(*buttons)



integration_kb = types.InlineKeyboardMarkup()
integration_button = [
    types.KeyboardButton(text='Discord', url='Ссылка')
]
integration_kb.add(*integration_button)



func_kb = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 3)
func_kb_buttons = [
    types.KeyboardButton(text = 'Показать задачи'),
    types.KeyboardButton(text = 'Добавить задачу'),
    types.KeyboardButton(text = 'Удалить задачу'),
    types.KeyboardButton(text = 'Выполнил задачу'),
    types.KeyboardButton(text = 'Назад')
]
func_kb.add(*func_kb_buttons)
