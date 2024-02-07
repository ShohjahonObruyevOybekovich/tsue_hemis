
import httpx
from aiogram.client import bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bs4 import BeautifulSoup
from sqlalchemy import insert
from aiogram import types
from bot.buttons.reply import menu_btn, start_menu, women_month, men_month
from bot.buttons.text import *
from db.connect import session
from db.model import User
from dispatcher import dp


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

@dp.message(lambda msg: msg.text == admin_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer_photo(photo='https://telegra.ph/file/3f3c0fec9b8c87882c4ce.png',
        caption="Obruyev Shohjahon \n https://t.me/shokh_its_me",
        reply_markup=menu_btn())


@dp.message(lambda msg : msg.text == start_txt)
async def register_handler(msg : Message , state : FSMContext):
    await msg.answer("Quydagilardan birontasini tanlang 👇🏿!", reply_markup=start_menu())



@dp.message(lambda msg: msg.text == news)
async def get_news(msg: Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://kun.uz/")

        if response.status_code == 200:
            html_doc = response.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            news_list = []

            for item in soup.find_all("div", {"class": "top-news__item"}):
                news_title = item.find("a", {"class": "top-news__item-title"}).text.strip()
                news_link = item.find("a", {"class": "top-news__item-title"})['href']
                news_image = item.find("img", {"class": "top-news__item-image"})['src']
                news_list.append((news_title, news_link, news_image))

            await msg.bot.send_message(msg.chat.id, "Welcome! Here are the latest news articles from kun.uz:")

            news_articles = news_list[:4]
            for news_title, news_link, news_image in news_articles:
                news_caption = f"<b>{news_title}</b>\n{news_link}"
                await msg.bot.send_photo(msg.chat.id, photo=news_image, caption=news_caption,
                                      parse_mode=types.ParseMode.HTML)
    except Exception as e:
        print(f"An error occurred while fetching news: {str(e)}")
@dp.message(lambda msg: msg.text == women_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer_photo(photo='https://telegra.ph/file/5e5e265ae6e265becc39b.png',
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


