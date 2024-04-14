from aiogram.fsm.state import State, StatesGroup


class RequestForm(StatesGroup):
    select_type = State()
    for_who_request = State()
    select_delivery_type = State()
    enter_request = State()
    enter_contact_first_name = State()
    enter_contact_last_name = State()
    enter_contact_phone_number = State()
    choose_request_address = State()
    enter_request_region = State()
    enter_request_city = State()
    enter_request_street = State()
    enter_request_house_number = State()
    enter_request_flat_number = State()
