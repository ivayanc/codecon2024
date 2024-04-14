from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, and_
from datetime import datetime

from database.base import session

from bot.utils.keyboards import MainKeyboards, EvacuationKeyboards
from bot.states.evacuation import EvacuationForm
from bot.utils.enums import EvacuationRequestStatus
from bot.utils.database import get_regions
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
    if call.data == 'evacuation_for_me':
        user_id = call.from_user.id
        with session() as s:
            user = s.query(User).filter(User.telegram_id == user_id).first()
            user_region = s.query(UserRegion).filter(and_(UserRegion.user_id == user_id,
                                                          UserRegion.volunteer_region == False)).first()
            await state.update_data(first_name=user.first_name)
            await state.update_data(last_name=user.last_name)
            await state.update_data(phone_number=user.phone_number)
            await state.update_data(city=user.city)
            await state.update_data(street=user.street)
            await state.update_data(home_number=user.house_number)
            await state.update_data(flat_number=user.flat_number)
            await state.update_data(region_id=user_region.region_id)
        await state.set_state(EvacuationForm.choose_evacuation_address)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('evacuation_prompts', 'choose_evacuation_address'),
            reply_markup=MainKeyboards.yes_no_keyboard()
        )
    else:
        await state.set_state(EvacuationForm.enter_contact_first_name)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('evacuation_prompts', 'enter_contact_first_name'),
            reply_markup=None
        )


@evacuation_router.message(EvacuationForm.enter_contact_first_name)
async def enter_contact_first_name(message: Message, state: FSMContext) -> None:
    contact_first_name = message.text
    await state.update_data(first_name=contact_first_name)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_contact_last_name'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_contact_last_name)


@evacuation_router.message(EvacuationForm.enter_contact_last_name)
async def enter_contact_last_name(message: Message, state: FSMContext) -> None:
    contact_last_name = message.text
    await state.update_data(last_name=contact_last_name)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_contact_phone_number'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_contact_phone_number)


@evacuation_router.message(EvacuationForm.enter_contact_phone_number)
async def enter_contact_phone_number(message: Message, state: FSMContext) -> None:
    contact_phone_number = message.text
    await state.update_data(phone_number=contact_phone_number)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'choose_evacuation_address'),
        reply_markup=MainKeyboards.yes_no_keyboard()
    )
    await state.set_state(EvacuationForm.choose_evacuation_address)


@evacuation_router.callback_query(EvacuationForm.choose_evacuation_address)
async def choose_evacuation_address(call: CallbackQuery, state: FSMContext) -> None:
    if call.data == 'yes':
        await state.set_state(EvacuationForm.enter_evacuation_qnt)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('evacuation_prompts', 'enter_evacuation_qnt'),
            reply_markup=None
        )
    else:
        regions = await get_regions()
        await state.set_state(EvacuationForm.enter_evacuation_region)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('evacuation_prompts', 'enter_evacuation_region'),
            reply_markup=MainKeyboards.region_keyboard(regions)
        )


@evacuation_router.callback_query(EvacuationForm.enter_evacuation_region)
async def enter_evacuation_region(call: CallbackQuery, state: FSMContext):
    await state.update_data(region_id=int(call.data))
    await state.set_state(EvacuationForm.enter_evacuation_city)
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_city'),
        reply_markup=None
    )


@evacuation_router.message(EvacuationForm.enter_evacuation_city)
async def enter_evacuation_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_street'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_evacuation_street)


@evacuation_router.message(EvacuationForm.enter_evacuation_street)
async def enter_evacuation_street(message: Message, state: FSMContext) -> None:
    await state.update_data(street=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_house_number'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_evacuation_house_number)


@evacuation_router.message(EvacuationForm.enter_evacuation_house_number)
async def enter_evacuation_house_number(message: Message, state: FSMContext) -> None:
    await state.update_data(home_number=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_flat_number'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_evacuation_flat_number)


@evacuation_router.message(EvacuationForm.enter_evacuation_flat_number)
async def enter_evacuation_flat_number(message: Message, state: FSMContext) -> None:
    await state.update_data(flat_number=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('evacuation_prompts', 'enter_evacuation_qnt'),
        reply_markup=None
    )
    await state.set_state(EvacuationForm.enter_evacuation_qnt)


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
        else:
            await state.update_data(evacuation_qnt=evacuation_qnt)
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
            contact_last_name=data.get('last_name', ''),
            contact_phone_number=data.get('phone_number', ''),
            evacuation_qnt=data.get('evacuation_qnt', 1),
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


@evacuation_router.callback_query(F.data.startswith('selectevacuationrate_'))
async def process_rate_select(call: CallbackQuery) -> None:
    _, request_id, rate = call.data.split('_')
    request_id = int(request_id)
    rate = int(rate)
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ua_config.get('evacuation_prompts', 'volunteer_finish'),
        reply_markup=None
    )
