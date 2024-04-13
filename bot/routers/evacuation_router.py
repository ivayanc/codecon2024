from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from datetime import datetime

from database.base import session

from bot.utils.keyboards import MainKeyboards, EvacuationKeyboards
from bot.states.evacuation import EvacuationForm
from bot.utils.enums import EvacuationRequestStatus
from configuration import ua_config
from database.models.user import User
from database.models.user_region import UserRegion
from database.models.evacuation_requests import EvacuationRequest

evacuation_router = Router()


@evacuation_router.message(F.text == ua_config.get('main_menu', 'request_evacuation'))
async def evacuation_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'for_who_evacuation'),
        reply_markup=EvacuationKeyboards.evacuation_for_who()
    )
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(EvacuationForm.for_who_evacuation)


@evacuation_router.callback_query(EvacuationForm.for_who_evacuation)
async def process_region_selection(call: CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    with session() as s:
        user = s.query(User).filter(User.telegram_id == user_id).first()
        user_region = s.query(UserRegion).filter(UserRegion.user_id == user_id).first()
        await state.update_data(first_name=user.first_name)
        await state.update_data(last_name=user.last_name)
        await state.update_data(phone_number=user.phone_number)
        await state.update_data(city=user.city)
        await state.update_data(street=user.street)
        await state.update_data(house_number=user.house_number)
        await state.update_data(flat_number=user.flat_number)
        await state.update_data(region_id=user_region.region_id)
    await state.set_state(EvacuationForm.enter_evacuation_qnt)
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_qnt'),
        reply_markup=None
    )


async def send_wrong_evacuation_qnt_error(message: Message) -> None:
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_qnt'),
        reply_markup=None
    )


@evacuation_router.message(EvacuationForm.enter_evacuation_qnt)
async def process_evacuation_qnt(message: Message, state: FSMContext) -> None:
    ss = await state.get_state()
    evacuation_qnt = message.text
    try:
        evacuation_qnt = int(evacuation_qnt)
        if evacuation_qnt > 4 or evacuation_qnt <= 0:
            await send_wrong_evacuation_qnt_error(message)
        await state.set_state(EvacuationForm.any_special_needs)
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=ua_config.get('evacuation_prompts', 'special_need_question'),
            reply_markup=MainKeyboards.yes_no_keyboard()
        )
    except ValueError as e:
        await send_wrong_evacuation_qnt_error(message)


async def finish_request(message: Message, state: FSMContext, edit_message: bool = False):
    data = await state.get_data()
    with session() as s:
        evacuation_requests = EvacuationRequest(
            region_id=int(data.get('region_id', 0)),
            user_id=int(data.get('user_id', 0)),
            city=data.get('city', ''),
            street=data.get('street', ''),
            home_number=data.get('home_number', ''),
            flat_number=data.get('flat_number', ''),
            contact_first_name=data.get('first_name', ''),
            contact_last_name=data.get('contact_last_name', ''),
            contact_phone_number=data.get('phone_number', ''),
            any_special_needs=data.get('any_special_needs', False),
            special_needs=data.get('special_needs', ''),
            request_date=datetime.now(),
            request_status=EvacuationRequestStatus.created
        )
        s.add(evacuation_requests)
        s.commit()

    if edit_message:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=ua_config.get('evacuation_prompts', 'request_accepted'),
            reply_markup=None
        )
    else:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=ua_config.get('evacuation_prompts', 'request_accepted'),
            reply_markup=None
        )
    await state.clear()


@evacuation_router.callback_query(EvacuationForm.any_special_needs)
async def process_any_special_needs(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    if call.data == 'yes':
        await state.update_data(any_special_needs=True)
        await state.set_state(EvacuationForm.special_needs)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('evacuation_prompts', 'special_need'),
            reply_markup=None
        )
    else:
        await state.update_data(any_special_needs=False)
        await finish_request(call.message, state, True)


@evacuation_router.message(EvacuationForm.special_needs)
async def process_special_needs(message: Message, state: FSMContext) -> None:
    await state.update_data(special_needs=message.text)
    await finish_request(message, state)
