from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.buttons.text import *

def from_whom_menu():
    uz_btn = InlineKeyboardButton(text=teachers_txt, callback_data=teachers_txt)
    en_btn = InlineKeyboardButton(text=Administratsiya_txt, callback_data=Administratsiya_txt)
    other_btn = InlineKeyboardButton(text=Others_txt, callback_data=Others_txt)
    return InlineKeyboardMarkup(inline_keyboard=[[uz_btn ],[ en_btn],[other_btn]])


def takliflar_from_whom_menu():
    tashkiliy_btn = InlineKeyboardButton(text=Tashkiliy_txt,callback_data=Tashkiliy_txt)
    media_btn = InlineKeyboardButton(text=Media_txt, callback_data=Media_txt)
    other_btn = InlineKeyboardButton(text=Others_txt,callback_data=Others_txt)
    design = [
        [tashkiliy_btn],
        [media_btn],
        [other_btn]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)