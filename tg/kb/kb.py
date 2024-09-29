from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def tickets_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Добавить поставку", callback_data='add'),InlineKeyboardButton(text="Удалить поставку", callback_data='delete')],
        [InlineKeyboardButton(text="Показать поставки", callback_data='show'),InlineKeyboardButton(text="Cбросить поставки", callback_data='reset')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list, row_width = 2)