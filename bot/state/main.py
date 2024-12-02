from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    Student_login=State()
    Student_password=State()

class JadvalState(StatesGroup):
    semestr = State()
    semestr1 = State()
    fan = State()
    unm = State()
