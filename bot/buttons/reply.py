from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.text import *


def menu_btn():
    k1 = KeyboardButton(text = filial_txt)
    k2 = KeyboardButton(text = start_txt)
    k3 = KeyboardButton(text =news)
    k4 = KeyboardButton(text=admin_txt)
    design = [
        [k1 , k2],
        [k3],
        [k4]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)


def start_menu():
    k1 = KeyboardButton(text = women_txt)
    k2 = KeyboardButton(text = men_txt)
    k3 = KeyboardButton(text = back_txt)
    design = [
        [k1 , k2],
        [k3]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)
def women_month():
    k1 = KeyboardButton(text = oy1)
    k2 = KeyboardButton(text = oy2)
    k3 = KeyboardButton(text = oy3)
    k4 = KeyboardButton(text =oy4)
    k5 = KeyboardButton(text=back_txt)
    design = [
        [k1 , k2],
        [k3, k4],
        [k5]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

def men_month():
    k1 = KeyboardButton(text = oy1)
    k2 = KeyboardButton(text = oy2)
    k3 = KeyboardButton(text = oy3)
    k4 = KeyboardButton(text =oy4)
    k5 = KeyboardButton(text=back_txt)
    design = [
        [k1 , k2],
        [k3, k4],
        [k5]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)
