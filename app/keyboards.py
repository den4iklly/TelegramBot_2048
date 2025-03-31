from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=' '), KeyboardButton(text='up'), KeyboardButton(text=' ')],
    [KeyboardButton(text='left'), KeyboardButton(text=' '), KeyboardButton(text='right')],
    [KeyboardButton(text=' '), KeyboardButton(text='down'), KeyboardButton(text=' ')]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")


def create_kb_2048(values):
    kb_2048 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=v, callback_data='some_data') for v in values[i]] for i in range(len(values))
    ])
    return kb_2048
