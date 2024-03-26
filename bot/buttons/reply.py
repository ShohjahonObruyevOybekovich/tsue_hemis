from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.text import *


def menu_btn():
    k1 = KeyboardButton(text = shikoyat_txt)
    k2 = KeyboardButton(text = taklif_txt)
    # k4 = KeyboardButton(text=admin_txt)
    design = [
        [k1 , k2]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

