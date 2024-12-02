from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.text import *


def menu_btn():
    k1 = KeyboardButton(text = dars_jadvali_txt)
    k2 = KeyboardButton(text = talaba_info_txt)
    k3 = KeyboardButton(text = baholar_txt)
    k4 = KeyboardButton(text=admin)
    design = [
        [k1 , k2],
        [k3 , k4],
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

def Login():
    keyboard1 = KeyboardButton(text = Login_txt)
    design = [[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)



def admin_btn():
    keyboard1 = KeyboardButton(text = admin_shikoyat_list_txt)
    keyboard2 = KeyboardButton(text = admin_back_menu_txt)
    design = [[keyboard1, keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)