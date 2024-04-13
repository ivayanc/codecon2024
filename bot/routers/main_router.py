from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types.contact import Contact
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.fsm.context import FSMContext

from bot.utils.keyboards import MainKeyboards
from bot.states.profile_managment import RegisterForm

from configuration import ua_config

main_router = Router()


async def send_welcome_message(message: Message, edit_message: bool = False) -> None:
    welcome_text = ua_config.get('prompts', 'start_message')
    if edit_message:
        await message.bot.delete_message(chat_id=message.chat.id,
                                         message_id=message.message_id)
    await message.answer(welcome_text)


@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await send_welcome_message(message)
    await state.set_state(RegisterForm.first_name)
    await message.bot.send_message(text=ua_config.get('registration', 'enter_first_name'),
                                   chat_id=message.chat.id,
                                   reply_markup=ReplyKeyboardRemove())


@main_router.message(RegisterForm.first_name)
@main_router.message(RegisterForm.last_name)
@main_router.message(RegisterForm.birthday_date)
@main_router.message(RegisterForm.region)
@main_router.message(RegisterForm.city)
@main_router.message(RegisterForm.street)
@main_router.message(RegisterForm.house_number)
async def process_manage_profile_reply(message: Message, state: FSMContext):
    await state.update_data(reply_info=message.text)
    await message.reply(ua_config.get(
        'prompts', 'validate_data'
    ).format(data=message.text), reply_markup=MainKeyboards.validate_keyboard())


@main_router.callback_query(F.data == 'validate')
async def process_validate_callback(call: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    data = await state.get_data()
    new_message = False
    reply_markup = None
    text = 'Please use keyboard'
    if current_state == RegisterForm.first_name.state:
        await state.update_data(first_name=data.get('reply_info'))
        await state.set_state(RegisterForm.last_name)
        text = ua_config.get('registration', 'enter_last_name')
    if current_state == RegisterForm.last_name.state:
        await state.update_data(last_name=data.get('reply_info'))
        await state.set_state(RegisterForm.birthday_date)
        text = ua_config.get('registration', 'enter_birthday_date')
    if current_state == RegisterForm.birthday_date.state:
        await state.update_data(last_name=data.get('reply_info'))
        await state.set_state(RegisterForm.share_phone_number)
        text = ua_config.get('registration', 'share_phone_number')
        reply_markup = MainKeyboards.share_contact_keyboard()
        new_message = True
    if new_message:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.bot.send_message(chat_id=call.message.chat.id,
                                    text=text,
                                    reply_markup=reply_markup)
    else:
        await call.bot.edit_message_text(message_id=call.message.message_id,
                                         chat_id=call.message.chat.id,
                                         text=text,
                                         reply_markup=reply_markup)
