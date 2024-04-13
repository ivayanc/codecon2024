from aiogram.fsm.state import State, StatesGroup


class RequestForm(StatesGroup):
    select_type = State()
    for_who_request = State()
    select_delivery_type = State()
    enter_request = State()
