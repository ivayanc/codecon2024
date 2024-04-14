from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from datetime import datetime

from database.base import session

from bot.utils.keyboards import GovernmentHelpKeyboards
from bot.states.requests import RequestForm
from bot.utils.enums import RequestType, RequestStatus
from bot.utils.database import get_request_types
from configuration import ua_config
from database.models.user import User
from database.models.user_region import UserRegion
from database.models.request import Request

government_help_router = Router()


@government_help_router.message(F.text == ua_config.get('main_menu', 'ask_government_help'))
async def government_help_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=ua_config.get('government_help', 'select_category'),
        reply_markup=GovernmentHelpKeyboards.main_inline_keyboard()
    )


@government_help_router.callback_query(F.data == 'first_option')
@government_help_router.callback_query(F.data == 'second_option')
@government_help_router.callback_query(F.data == 'third_option')
@government_help_router.callback_query(F.data == 'fourth_option')
async def government_help_handler(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = 'Wrong'
    if call.data == 'first_option':
        text = ua_config.get('government_help', 'first_option_answer')
    if call.data == 'second_option':
        text = ua_config.get('government_help', 'second_option_answer')
    if call.data == 'third_option':
        text = ua_config.get('government_help', 'third_option_answer')
    if call.data == 'fourth_option':
        text = ua_config.get('government_help', 'fourth_option_answer')
    await call.message.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=None,
        disable_web_page_preview=True
    )
