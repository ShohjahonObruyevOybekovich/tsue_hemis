import urllib
from collections import defaultdict

import urllib
from collections import defaultdict

import requests
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientSession
from icecream import ic  # Assuming you're using the 'icecream' library for debugging
from sqlalchemy import insert, update

from bot.buttons.inline import *
from bot.buttons.reply import menu_btn, Login
from bot.buttons.text import *
from bot.state.main import UserState, JadvalState
from db.connect import session
from db.model import User
from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Assalomu alaykum <b><i>{message.from_user.username}</i></b> \nBotdan foydalanish uchun avval malumotlaringizni to'ldiring👇🏿",
        parse_mode="HTML",  # Enable HTML parsing
        reply_markup=Login()
    )

    try:
        # Query the database to find a user with the given ID
        user = session.query(User).filter(User.chat_id == message.from_user.id).first()

        # Check if the user exists
        if user:
            print("User is already registered:", user)

        else:
            print("User is not registered.")
            query = insert(User).values(chat_id=message.from_user.id)
            session.execute(query)
            session.commit()

    except Exception as e:
        print(f"Error checking user registration: {e}")





@dp.message(lambda msg : msg.text == Login_txt)
async def register_handler(msg : Message , state : FSMContext):
    await state.set_state(UserState.Student_login)
    await msg.answer(" Student hemis loginingizni kiriting👇🏿!")

@dp.message(UserState.Student_login)
async def login(msg : Message , state : FSMContext):
    data = await state.get_data()
    data["Student_login"] = msg.text
    await state.set_data(data)
    await state.set_state(UserState.Student_password)
    await msg.answer(text='Parolni kiriting ✏️')

@dp.message(UserState.Student_password)
async def handle_password(msg: Message, state: FSMContext):
    # Get the data stored in state
    user_data = await state.get_data()
    login = user_data.get("Student_login")
    password = msg.text

    # Prepare the API request
    url = "https://talaba.tsue.uz/rest/v1/auth/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {
        "login": login,
        "password": password
    }

    # Send the request to the API
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("success"):
            token = response_data["data"]["token"]
            query = update(User).values(login_code = login,password=password, token = token).where(User.chat_id == msg.from_user.id)
            session.execute(query)
            session.commit()
            await msg.answer(f"✅ Muvaffaqiyatli login qilindi!\n", reply_markup=menu_btn())
        else:
            error_message = response_data.get("error", "Noma'lum xato yuz berdi.")
            print(error_message)
            await msg.answer(f"❌ Xatolik yuz berdi 1",reply_markup=Login())

    except Exception as e:
        print(e)
        await msg.answer(f"❌ Xatolik yuz berdi",reply_markup=Login())

    # Reset the state after processing
    await state.clear()










#davomat
@dp.message(lambda msg: msg.text == davomad_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer("Semestrni tanlang:", reply_markup=semestr())
    await state.set_state(JadvalState.semestr)



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.callback_query(JadvalState.semestr)
async def from_whom_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    token = session.query(User).filter(User.chat_id == call.from_user.id).first()
    if not token:
        await call.message.answer("User not registered. Please register first.")
        return

    headers = {"Authorization": f"Bearer {token.token}", "Accept": "application/json"}
    semester = call.data
    schedule_url = f"https://talaba.tsue.uz/rest/v1/education/subject-list?semester={semester}"

    response = requests.get(schedule_url, headers=headers)


    if response.status_code != 200:
        await call.message.answer(f"Failed to fetch data for semester {semester}.")
        return

    response_data = response.json()
    subjects = response_data.get("data", [])
    if not subjects:
        await call.message.answer(f"No subjects found for semester {semester}.")
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    for subject in subjects:
        subject_name = subject.get("curriculumSubject", {}).get("subject", {}).get("name")
        if subject_name:
            # URL-encode subject name to handle special characters
            callback_data = f"subject_{urllib.parse.quote(subject_name)}"
            ic(callback_data)

            # Append the button to inline_keyboard directly
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=subject_name, callback_data=callback_data)])

    await call.message.answer("Select a subject:", reply_markup=keyboard)
    await state.set_state(JadvalState.unm)



# @dp.callback_query(lambda c: c.data.startswith("subject_"))
@dp.callback_query(JadvalState.unm)
async def subject_info_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["unm"] = call.data
    try:
        subject_name = urllib.parse.unquote(call.data[len("subject_"):])
        ic(f"Decoded subject name: {subject_name}")

        token = session.query(User).filter(User.chat_id == call.from_user.id).first()
        if not token:
            await call.message.answer("User not registered. Please register first.")
            return

        headers = {"Authorization": f"Bearer {token.token}", "Accept": "application/json"}
        schedule_url = "https://talaba.tsue.uz/rest/v1/education/subject-list"
        response = requests.get(schedule_url, headers=headers)

        if response.status_code != 200:
            await call.message.answer("Failed to fetch subject list.")
            return

        response_data = response.json()
        subjects = response_data.get("data", [])
        ic(subjects)
        selected_subject = next(
            (sub for sub in subjects if sub.get("curriculumSubject", {}).get("subject", {}).get("name") == subject_name),
            None,
        )

        if not selected_subject:
            await call.message.answer(f"Subject {subject_name} not found.")
            return

        subject_info = selected_subject.get("curriculumSubject", {}).get("subject", {})
        subject_type = selected_subject.get("curriculumSubject", {}).get("subjectType", {}).get("name", "Unknown")
        credits = selected_subject.get("curriculumSubject", {}).get("credit", "N/A")
        total_acload = selected_subject.get("curriculumSubject", {}).get("total_acload", "N/A")
        grades = selected_subject.get("gradesByExam", [])

        response_text = f"*Subject:* {subject_info.get('name', 'Unknown')}\n"
        response_text += f"*Code:* {subject_info.get('code', 'N/A')}\n"
        response_text += f"*Type:* {subject_type}\n"
        response_text += f"*Credits:* {credits}\n"
        response_text += f"*Total Acload:* {total_acload}\n"



        if grades:
            for grade in grades:
                exam_type = grade.get("examType", {}).get("name", "Unknown")
                grade_value = grade.get("grade", "N/A")
                response_text += f"{exam_type}: {grade_value}\n"

        await call.message.answer(response_text,parse_mode='Markdown')

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        await call.message.answer(f"An error occurred: {str(e)}")
    await state.clear()













from datetime import datetime, timedelta
@dp.message(lambda msg: msg.text == dars_jadvali_txt)
async def dars_advali(msg: Message, state: FSMContext):
    await msg.answer("Semestrni tanlang:", reply_markup=semestr())
    await state.set_state(JadvalState.semestr1)

@dp.callback_query(JadvalState.semestr1)
async def from_whom_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["semestr1"] = call.data
    print(call.data)
    await call.message.delete()
    try:
        # Retrieve user token
        token_entry = session.query(User).filter(User.chat_id == call.from_user.id).first()
        if not token_entry:
            await call.message.answer("Kirishda muammo, iltimos shaxsingizni tasdiqlang", reply_markup=Login())
            return

        token = token_entry.token
        headers = {
            "Authorization": f"Bearer {token}",
            
            "Accept": "application/json"
        }

        schedule_url = f"https://talaba.tsue.uz/rest/v1/education/schedule?semester={call.data}"

        # Calculate the last week's date range
        today = datetime.now()
        last_week_start = today - timedelta(days=today.weekday() + 8)  # Start of last week
        last_week_end = last_week_start + timedelta(days=6)  # End of last week

        async with ClientSession() as sess:
            async with sess.get(schedule_url, headers=headers) as response:
                if response.status == 200:
                    schedule_data = await response.json()
                    if schedule_data.get("success") and schedule_data.get("data"):
                        lessons_by_day = defaultdict(list)

                        for lesson in schedule_data["data"]:
                            lesson_date = lesson.get("lesson_date")
                            if not lesson_date:
                                continue

                            # Parse lesson date to datetime
                            lesson_date = datetime.fromisoformat(lesson_date) if isinstance(lesson_date, str) else datetime.utcfromtimestamp(lesson_date)

                            # Check if the lesson is within the last week's range
                            if last_week_start <= lesson_date <= last_week_end:
                                lessons_by_day[lesson_date].append(lesson)

                        if not lessons_by_day:
                            await call.message.answer("O'tgan haftaning jadvali mavjud emas.")
                            return

                        # Send grouped lessons for each day
                        for lesson_date, lessons in sorted(lessons_by_day.items()):
                            day_name = lesson_date.strftime("%Y-%m-%d (%A)")
                            day_schedule = f"📅 Sana: {day_name}\n\n"

                            for lesson in lessons:
                                subject = lesson["subject"]["name"]
                                subject_code = lesson["subject"]["code"]
                                lesson_type = lesson["trainingType"]["name"]
                                location = f"{lesson['auditorium']['name']} ({lesson['auditorium']['building']['name']})"
                                start_time = lesson["lessonPair"]["start_time"]
                                end_time = lesson["lessonPair"]["end_time"]
                                teacher = lesson["employee"]["name"]

                                day_schedule += (
                                    f"📚 {subject} ({subject_code}) - {lesson_type}\n"
                                    f"🚪 Auditoriya: {location}\n"
                                    f"🕔 Dars vaqti: {start_time} - {end_time}\n"
                                    f"👨‍🏫 O'qituvchi: {teacher}\n"
                                    "_______\n\n"
                                )

                            # Split large messages into chunks
                            for chunk in split_message(day_schedule):
                                await call.message.answer(chunk)
                    else:
                        await call.message.answer("Sizning dars jadvalingiz mavjud emas yoki to'liq emas.")
                elif response.status == 401:
                    await call.message.answer("Sizning tokeningiz yaroqsiz yoki muddati o'tgan.")
                else:
                    error_detail = await response.text()
                    await call.message.answer(f"Jadvalni olishda xatolik yuz berdi: {error_detail}")

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        await call.message.answer(f"Xato yuz berdi:\n{error_trace}")
    await state.clear()


def split_message(message, max_length=4096):
    """
    Splits a message into chunks of at most `max_length` characters.
    """
    parts = []
    while len(message) > max_length:
        # Find the last newline character within the limit
        split_index = message.rfind("\n", 0, max_length)
        if split_index == -1:  # No newline found, split at max_length
            split_index = max_length
        parts.append(message[:split_index])
        message = message[split_index:].strip()
    parts.append(message)
    return parts









#student info
@dp.message(lambda msg : msg.text == talaba_info_txt)
async def talaba_info(msg: Message, state: FSMContext):
    try:
        # Fetch user token from the database
        token = session.query(User).filter(User.chat_id == msg.from_user.id).first()
        if token:
            headers = {
                "Authorization": f"Bearer {token.token}",
                "Accept": "application/json"
            }

            # URL to get account information
            me_url = "https://talaba.tsue.uz/rest/v1/account/me"
            response = requests.get(me_url, headers=headers)

            if response.status_code == 200:
                student_data = response.json().get("data", {})

                # Extract relevant student info
                full_name = student_data.get("full_name", "N/A")
                phone = student_data.get("phone", "N/A")
                semester = student_data.get("semester", {}).get("name", "N/A")
                address = student_data.get("address", "N/A")
                image_url = student_data.get("image", "")
                group_name = student_data.get("group", {}).get("name", "N/A")
                faculty_name = student_data.get("faculty", {}).get("name", "N/A")
                level_name = student_data.get("level", {}).get("name", "N/A")

                # Format the response message
                formatted_message = (
                    "🎓 **Student Information**\n"
                    "#### 🏫 **Toshkent davlat iqtisodiyot universiteti**\n\n"
                    f"**👤 Full Name:**\n`{full_name}`\n\n"
                    f"**🏫 Faculty:**\n`{faculty_name}`\n\n"
                    f"**👥 Group:**\n`{group_name}`\n\n"
                    f"**🎓 Level:**\n`{level_name}`\n\n"
                    f"**📱 Phone Number:**\n`{phone}`\n\n"
                    f"**📚 Semester:**\n`{semester}`\n\n"
                    f"**🏡 Address:**\n`{address}`\n\n"
                )

                # Send the profile picture first, then the text
                if image_url:
                    # Send image first with caption containing the formatted message
                    await msg.answer_photo(image_url, caption=formatted_message)
                else:
                    # If no image URL, just send the formatted message
                    await msg.answer(formatted_message)

            elif response.status_code == 401:
                await msg.answer(text="Unauthorized: Your token might be invalid or expired.")
            else:
                await msg.answer(text=f"Failed to fetch account info: {response.json()}")
        else:
            # If no token found
            await msg.answer(text="Kirishda muammo, iltimos shaxsingizni tasdiqlang", reply_markup=Login())
    except Exception as e:
        print(f"Error checking user registration: {e}")
        await msg.answer(text="Iltimos, xatolik yuz berdi. Qayta urinib ko'ring.")

@dp.message(lambda msg : msg.text == admin)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer(
        text="Bot <b><i>IT klub</i></b> tomonidan ishlab chiqildi\nBot haqida qo'shimcha takliflar uchun dasturchiga murojat qilishingiz mumkin 👉 <a href='https://t.me/shokh_smee'>Dasturchi</a>",
        reply_markup=menu_btn(),
        parse_mode="HTML"
    )


async def fetch_semesters(token: str):
    url = "https://student.hemis.uz/rest/v1/education/semesters"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["success"]:
            return data["data"]
        else:
            return None # Handle errors appropriately.  Could return an empty list []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching semesters: {e}")
        return None


