from aiogram.fsm.state import State, StatesGroup


class EvacuationForm(StatesGroup):
    for_who_evacuation = State()
    enter_evacuation_qnt = State()
    any_special_needs = State()
    special_needs = State()

