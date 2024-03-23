from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    from_whom=State()
    message=State()
class TaklifState(StatesGroup):
    from_whom=State()
    message=State()



