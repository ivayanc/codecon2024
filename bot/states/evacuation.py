from aiogram.fsm.state import State, StatesGroup


class EvacuationForm(StatesGroup):
    for_who_evacuation = State()
    enter_evacuation_qnt = State()
    any_special_needs = State()
    special_needs = State()
    enter_contact_first_name = State()
    enter_contact_last_name = State()
    enter_contact_phone_number = State()
    choose_evacuation_address = State()
    enter_evacuation_region = State()
    enter_evacuation_city = State()
    enter_evacuation_street = State()
    enter_evacuation_house_number = State()
    enter_evacuation_flat_number = State()
