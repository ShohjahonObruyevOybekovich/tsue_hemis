from select import select

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic  # Assuming you're using the 'icecream' library for debugging
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from bot.buttons.inline import *
from bot.buttons.reply import menu_btn
from bot.buttons.text import *
from bot.state.main import UserState, TaklifState
from db.connect import session
from db.model import User
from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer_photo(
        photo='https://telegra.ph/file/4aededade39de77dc3d55.png',
        caption="Assalomu alaykum ! \nBu bot anonim tarzida ishlaydi. Bu yerda siz shikoyatlar yoki takliflaringizni qoldirishingiz mumkin va biz ularni o'rganib chiqamiz !",
        reply_markup=menu_btn()
    )
    query = insert(User).values(chat_id=message.from_user.id)
    session.execute(query)
    session.commit()

@dp.message(lambda msg: msg.text == admin_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer_photo(photo='https://telegra.ph/file/3f3c0fec9b8c87882c4ce.png',
        caption="Obruyev Shohjahon \n https://t.me/shokh_07me",
        reply_markup=menu_btn())

#shikoyatlar uchun
@dp.message(lambda msg : msg.text == shikoyat_txt)
async def register_handler(msg : Message , state : FSMContext):
    await state.set_state(UserState.from_whom)
    await msg.answer("Shikoyatlaringiz turini tanlang 👇🏿!", reply_markup=from_whom_menu())

@dp.callback_query(UserState.from_whom)
async def from_whom_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    data = await state.get_data()
    data["from_whom"] = call.data
    await state.set_data(data)
    await state.set_state(UserState.message)
    await call.message.answer(text='Shikoyatingizni kiriting ✏️')

@dp.message(UserState.message)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["message"] = msg.text
    user_messages = state_data["from_whom"]
    chat_id = msg.from_user.id
    ic(state_data)
    try:
        # Retrieve user data from the database
        database_data = session.execute(select(User.id, User.received_date).filter_by(chat_id=chat_id)).fetchone()

        # Prepare product string
        product = f"Message ID: {database_data[0]}\n"
        product += f"Kim haqida: {state_data.get('from_whom')}\n"
        product += f"Xabar matni: {state_data.get('message')}\n"
        product += f"Yuborilgan sana: {database_data[1]}\n"

        # Insert user message into the database
        session.execute(insert(User).values(chat_id=chat_id, user_messages=user_messages))
        session.commit()

        # Send message to admin
        await msg.bot.send_message(6729014582, text=product, reply_markup=menu_btn())
        await msg.bot.send_message(chat_id, text='Xabar yuborildi!', reply_markup=menu_btn())
        await state.clear()
    except SQLAlchemyError as e:
        # Handle any database errors
        ic(e)
        await msg.answer(text='Xatolik yuz berdi!', reply_markup=menu_btn())

# takliflar uchun
@dp.message(lambda msg : msg.text == taklif_txt)
async def takliflar_handler(msg : Message , state : FSMContext):
    await state.set_state(TaklifState.from_whom)
    await msg.answer("Takliflaringiz turini tanlang 👇🏿!", reply_markup=takliflar_from_whom_menu())

@dp.callback_query(TaklifState.from_whom)
async def from_whom_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    data = await state.get_data()
    data["from_whom"] = call.data
    await state.set_data(data)
    await state.set_state(UserState.message)
    await call.message.answer(text='Taklifingizni kiriting ✏️')

@dp.message(TaklifState.message)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["message"] = msg.text
    user_messages = state_data["from_whom"]
    chat_id = msg.from_user.id
    ic(state_data)
    try:
        # Retrieve user data from the database
        database_data = session.execute(select(User.id, User.received_date).filter_by(chat_id=chat_id)).fetchone()

        # Prepare product string
        product = f"Message ID: {database_data[0]}\n"
        product += f"Nima haqida: {state_data.get('from_whom')}\n"
        product += f"Xabar matni: {state_data.get('message')}\n"
        product += f"Yuborilgan sana: {database_data[1]}\n"

        # Insert user message into the database
        session.execute(insert(User).values(chat_id=chat_id, user_messages=user_messages))
        session.commit()

        # Send message to admin
        await msg.bot.send_message(6729014582, text=product, reply_markup=menu_btn())
        await msg.bot.send_message(chat_id, text='Xabar yuborildi!', reply_markup=menu_btn())
        await state.clear()
    except SQLAlchemyError as e:
        # Handle any database errors
        ic(e)
        await msg.answer(text='Xatolik yuz berdi!', reply_markup=menu_btn())

