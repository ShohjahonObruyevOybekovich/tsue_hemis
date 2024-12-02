from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.buttons.text import *


def semestr():
        first = InlineKeyboardButton(text='1 semestr', callback_data='11')
        second = InlineKeyboardButton(text='2 semestr', callback_data='12')
        third = InlineKeyboardButton(text='3 semestr', callback_data='13')
        fourth = InlineKeyboardButton(text='4 semestr', callback_data='14')
        fifth = InlineKeyboardButton(text='5 semestr', callback_data='15')
        sixth = InlineKeyboardButton(text='6 semestr', callback_data='16')
        seventh = InlineKeyboardButton(text='7 semestr', callback_data='17')
        eighth = InlineKeyboardButton(text='8 semestr', callback_data='18')
        design = [
            [first, second],
            [third, fourth],
            [fifth, sixth],
            [seventh, eighth]
        ]
        return InlineKeyboardMarkup(inline_keyboard=design)

