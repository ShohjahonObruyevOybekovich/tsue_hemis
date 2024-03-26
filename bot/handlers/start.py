from select import select

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic  # Assuming you're using the 'icecream' library for debugging
from sqlalchemy import select, insert, update,and_
from sqlalchemy.exc import SQLAlchemyError

from bot.buttons.inline import *
from bot.buttons.reply import menu_btn
from bot.buttons.text import *
from bot.state.main import UserState, TaklifState, AdminState
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



# #shikoyatlar uchun
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


@dp.message(lambda msg : msg.text == secret_key_admin)
async def register_handler(msg: Message, state: FSMContext):
    query = update(User).where(User.chat_id == msg.from_user.id).values(user_role='admin')
    session.execute(query)
    session.commit()
    await msg.answer(text="Sizning ID ma'lumotingiz saqlandi 😊",reply_markup=menu_btn())

@dp.message(UserState.message)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["message"] = msg.text
    user_messages = state_data.get("from_whom")  # Ensure to handle potential absence of key
    chat_id = msg.from_user.id

    try:
        # Retrieve admin IDs from the database
        Admin_id_list:list = session.execute(select(User.chat_id).where(User.user_role == 'admin')).fetchall()

        def remove_similar_strings(Admin_id_list):
            # Sort the list of Admin_id_list
            Admin_id_list.sort()

            # Initialize a result list with the first string
            result = [Admin_id_list[0]]

            # Iterate through the sorted list, skipping duplicates
            for i in range(1, len(Admin_id_list)):
                # If the current string is different from the previous one, add it to the result list
                if Admin_id_list[i] != Admin_id_list[i - 1]:
                    result.append(Admin_id_list[i])

            return result


        # Prepare product string
        database_data = session.execute(select(User.id, User.received_date).where(User.chat_id == chat_id)).fetchone()
        product = f"Message ID: {database_data[0]}\n\n"
        product += f"Kim haqida: {user_messages}\n\n"
        product += f"Xabar matni: {msg.text}\n\n"
        product += f"Yuborilgan sana: {database_data[1]}\n\n"

        # Insert user message into the database
        session.execute(
            insert(User).values(chat_id=int(chat_id), message_category=user_messages, user_messages=msg.text))
        session.commit()

        # Send messages to each admin
        for admin_data in remove_similar_strings(Admin_id_list):
            admin_chat_id = admin_data[0]
            ic(admin_chat_id)
            await msg.bot.send_message(admin_chat_id, text=product, reply_markup=menu_btn())

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
    user_messages = state_data.get("from_whom")  # Ensure to handle potential absence of key
    chat_id = msg.from_user.id

    try:
        # Retrieve admin IDs from the database
        Admin_id_list = session.execute(select(User.chat_id).where(User.user_role == 'admin')).fetchall()

        def remove_similar_strings(Admin_id_list):
            # Sort the list of Admin_id_list
            Admin_id_list.sort()

            # Initialize a result list with the first string
            result = [Admin_id_list[0]]

            # Iterate through the sorted list, skipping duplicates
            for i in range(1, len(Admin_id_list)):
                # If the current string is different from the previous one, add it to the result list
                if Admin_id_list[i] != Admin_id_list[i - 1]:
                    result.append(Admin_id_list[i])

            return result

        # Prepare product string
        database_data = session.execute(select(User.id, User.received_date).where(User.chat_id == chat_id)).fetchone()
        product = f"Message ID: {database_data[0]}\n\n"
        product += f"Nima haqida: {user_messages}\n\n"
        product += f"Xabar matni: {msg.text}\n\n"
        product += f"Yuborilgan sana: {database_data[1]}\n\n"

        # Insert user message into the database
        session.execute(insert(User).values(chat_id=chat_id, message_category=user_messages, user_messages=msg.text))
        session.commit()

        # Send messages to each admin
        for admin_data in remove_similar_strings(Admin_id_list):
            admin_chat_id = admin_data[0]
            ic(admin_chat_id)
            await msg.bot.send_message(admin_chat_id, text=product, reply_markup=menu_btn())

        await msg.bot.send_message(chat_id, text='Xabar yuborildi!', reply_markup=menu_btn())
        await state.clear()
    except SQLAlchemyError as e:
        # Handle any database errors
        ic(e)
        await msg.answer(text='Xatolik yuz berdi!', reply_markup=menu_btn())

