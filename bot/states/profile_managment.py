from aiogram.fsm.state import State, StatesGroup


class RegisterForm(StatesGroup):
    first_name = State()
    last_name = State()
    birthday_date = State()
    share_phone_number = State()
    region = State()
    city = State()
    street = State()
    house_number = State()
    flat_number = State()
