from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, and_
from datetime import datetime

from database.base import session

from bot.utils.keyboards import RequestKeyboards, MainKeyboards
from bot.states.requests import RequestForm
from bot.utils.enums import RequestType, RequestStatus
from bot.utils.database import get_request_types
from bot.utils.database import get_regions
from configuration import ua_config
from database.models.user import User
from database.models.user_region import UserRegion
from database.models.request import Request

request_router = Router()


@request_router.message(F.text == ua_config.get('main_menu', 'ask_volunteer_help'))
async def request_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    types = await get_request_types()
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'select_type'),
        reply_markup=RequestKeyboards.select_type(types)
    )
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(RequestForm.select_type)


@request_router.callback_query(RequestForm.select_type)
async def handle_request_type_select(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(type=call.data)
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ua_config.get('request_prompts', 'for_who_request'),
        reply_markup=RequestKeyboards.request_for_who()
    )
    await state.set_state(RequestForm.for_who_request)


@request_router.callback_query(RequestForm.for_who_request)
async def handle_for_who_request_response(call: CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    with session() as s:
        user = s.query(User).filter(User.telegram_id == user_id).first()
        user_region = s.query(UserRegion).filter(and_(UserRegion.user_id == user_id,
                                                      UserRegion.volunteer_region == False)).first()
        await state.update_data(region_id=user_region.region_id)
    if call.data == 'request_for_me':
        await state.update_data(first_name=user.first_name)
        await state.update_data(last_name=user.last_name)
        await state.update_data(phone_number=user.phone_number)
        await state.update_data(city=user.city)
        await state.update_data(street=user.street)
        await state.update_data(house_number=user.house_number)
        await state.update_data(flat_number=user.flat_number)
        await state.set_state(RequestForm.select_delivery_type)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'is_delivery'),
            reply_markup=RequestKeyboards.select_delivery_type()
        )
    else:
        await state.set_state(RequestForm.enter_contact_first_name)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'enter_contact_first_name'),
            reply_markup=None
        )


@request_router.message(RequestForm.enter_contact_first_name)
async def enter_contact_first_name(message: Message, state: FSMContext) -> None:
    contact_first_name = message.text
    await state.update_data(first_name=contact_first_name)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_contact_last_name'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_contact_last_name)


@request_router.message(RequestForm.enter_contact_last_name)
async def enter_contact_last_name(message: Message, state: FSMContext) -> None:
    contact_last_name = message.text
    await state.update_data(last_name=contact_last_name)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_contact_phone_number'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_contact_phone_number)


@request_router.message(RequestForm.enter_contact_phone_number)
async def enter_contact_phone_number(message: Message, state: FSMContext) -> None:
    contact_phone_number = message.text
    await state.update_data(phone_number=contact_phone_number)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'is_delivery'),
        reply_markup=RequestKeyboards.select_delivery_type()
    )
    await state.set_state(RequestForm.select_delivery_type)


@request_router.callback_query(RequestForm.select_delivery_type)
async def handle_delivery_type(call: CallbackQuery, state: FSMContext):
    await state.update_data(is_delivery=True if call.data == 'delivery' else False)
    if call.data == 'delivery':
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'choose_request_address'),
            reply_markup=MainKeyboards.yes_no_keyboard()
        )
        await state.set_state(RequestForm.choose_request_address)
    else:
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'enter_request_text'),
            reply_markup=None
        )
        await state.set_state(RequestForm.enter_request)


@request_router.callback_query(RequestForm.choose_request_address)
async def choose_request_address(call: CallbackQuery, state: FSMContext) -> None:
    if call.data == 'yes':
        await state.set_state(RequestForm.enter_request)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'enter_request_text'),
            reply_markup=None
        )
    else:
        regions = await get_regions()
        await state.set_state(RequestForm.enter_request_region)
        await call.message.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ua_config.get('request_prompts', 'enter_request_region'),
            reply_markup=MainKeyboards.region_keyboard(regions)
        )


@request_router.callback_query(RequestForm.enter_request_region)
async def enter_request_region(call: CallbackQuery, state: FSMContext):
    await state.update_data(region_id=int(call.data))
    await state.set_state(RequestForm.enter_request_city)
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ua_config.get('request_prompts', 'enter_request_city'),
        reply_markup=None
    )


@request_router.message(RequestForm.enter_request_city)
async def enter_request_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_request_street'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_request_street)


@request_router.message(RequestForm.enter_request_street)
async def enter_request_street(message: Message, state: FSMContext) -> None:
    await state.update_data(street=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_request_house_number'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_request_house_number)


@request_router.message(RequestForm.enter_request_house_number)
async def enter_request_house_number(message: Message, state: FSMContext) -> None:
    await state.update_data(home_number=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_request_flat_number'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_request_flat_number)


@request_router.message(RequestForm.enter_request_flat_number)
async def enter_request_flat_number(message: Message, state: FSMContext) -> None:
    await state.update_data(flat_number=message.text)
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'enter_request_text'),
        reply_markup=None
    )
    await state.set_state(RequestForm.enter_request)


@request_router.message(RequestForm.enter_request)
async def handle_request_text(message: Message, state: FSMContext):
    request_text = message.text
    data = await state.get_data()
    is_delivery = data.get('is_delivery', False)
    with session() as s:
        request = Request(
            request_text=request_text,
            is_delivery=is_delivery,
            city=data.get('city', '') if is_delivery else None,
            street=data.get('street', '') if is_delivery else None,
            home_number=data.get('home_number', '') if is_delivery else None,
            flat_number=data.get('flat_number', '') if is_delivery else None,
            region_id=int(data.get('region_id', 0)),
            user_id=int(data.get('user_id', 0)),
            contact_first_name=data.get('first_name', ''),
            contact_last_name=data.get('last_name', ''),
            contact_phone_number=data.get('phone_number', ''),
            type=RequestType(data.get('type', 0)).name,
            request_status=RequestStatus.created,
            request_date=datetime.now()
        )
        s.add(request)
        s.commit()
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('request_prompts', 'request_submitted')
    )
    await state.clear()
