from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert
from aiogram.methods.send_location import SendLocation
from bot.buttons.reply import menu_btn, start_menu, women_month, men_month
from bot.buttons.text import *
from db.connect import session
from db.model import User
from dispatcher import dp
from bs4 import BeautifulSoup
import httpx

@dp.message(CommandStart())
async def command_start_handler(message: Message, state : FSMContext) -> None:
    await message.answer_photo(
        photo='https://telegra.ph/file/905eebd66a046d0387746.jpg',
        caption="Assalomu alaykum ! \nBu bo'timiz sizga kunlik qiladigan 🏋️ mashqlarni ko'rsatib beradi",
        reply_markup=menu_btn()
    )
    query = insert(User).values(chat_id=message.from_user.id)
    session.execute(query)
    session.commit()

@dp.message(lambda msg : msg.text == filial_txt)
async def register_handler(msg : Message , state : FSMContext):
    await msg.answer("Location!")

@dp.message(lambda msg : msg.text == start_txt)
async def register_handler(msg : Message , state : FSMContext):
    await msg.answer("Quydagilardan birontasini tanlang 👇🏿!", reply_markup=start_menu())


@dp.message(lambda msg: msg.text == women_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer_photo(photo='https://telegra.ph/file/ef53fa0adc272ce176da3.jpg',
        caption="Quydagilarni birontasini tanlang 👇🏿",
        reply_markup=women_month())

@dp.message(lambda msg : msg.text ==back_women_txt)
async def back(msg : Message, state: FSMContext):
    await msg.answer('Menu 🏿', reply_markup=menu_btn())


@dp.message(lambda msg: msg.text == men_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer_photo(photo='https://telegra.ph/file/090a78542e8c4cd268a09.jpg',
        caption="Quydagilarni birontasini tanlang 👇🏿",
        reply_markup=men_month())

@dp.message(lambda msg : msg.text ==back_men_txt)
async def back(msg : Message, state: FSMContext):
    await msg.answer('Menu 🏿', reply_markup=menu_btn())


@dp.message(lambda msg : msg.text == news)
async def newsss(msg : Message, state:FSMContext):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://kun.uz/")
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    new=[]
    for i in soup.find_all("div", {"class": "single-layout"}):
        a = i.find("a", {"class": "single-layout_right"}).text.strip()
        new.append(a)
    await msg.answer(text=f'{new}', reply_markup=menu_btn())