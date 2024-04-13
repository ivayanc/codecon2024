from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types.contact import Contact
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.fsm.context import FSMContext

from bot.utils.keyboards import MainKeyboards
from bot.states.profile_managment import RegisterForm
from database.base import session
from database.models.user import User

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
@main_router.message(RegisterForm.flat_number)
async def process_manage_profile_reply(message: Message, state: FSMContext):
    await state.update_data(reply_info=message.text)
    await message.reply(ua_config.get(
        'prompts', 'validate_data'
    ).format(data=message.text), reply_markup=MainKeyboards.validate_keyboard())


@main_router.message(RegisterForm.share_phone_number)
async def process_manage_profile_reply(message: Message, state: FSMContext):
    if not message.contact:
        await message.bot.send_message('Please use keyboard')
    else:
        await state.update_data(phone_number=message.contact.phone_number)
        await state.set_state(RegisterForm.region)
        await message.reply(
            ua_config.get('registration', 'enter_region')
        )


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
    elif current_state == RegisterForm.last_name.state:
        await state.update_data(last_name=data.get('reply_info'))
        await state.set_state(RegisterForm.birthday_date)
        text = ua_config.get('registration', 'enter_birthday_date')
    elif current_state == RegisterForm.birthday_date.state:
        await state.update_data(birthday_date=data.get('reply_info'))
        await state.set_state(RegisterForm.share_phone_number)
        text = ua_config.get('registration', 'share_phone_number')
        reply_markup = MainKeyboards.share_contact_keyboard()
        new_message = True
    elif current_state == RegisterForm.region.state:
        await state.update_data(region=data.get('reply_info'))
        await state.set_state(RegisterForm.city)
        text = ua_config.get('registration', 'enter_city')
    elif current_state == RegisterForm.city.state:
        await state.update_data(city=data.get('reply_info'))
        await state.set_state(RegisterForm.street)
        text = ua_config.get('registration', 'enter_street')
    elif current_state == RegisterForm.street.state:
        await state.update_data(street=data.get('reply_info'))
        await state.set_state(RegisterForm.house_number)
        text = ua_config.get('registration', 'enter_house_number')
    elif current_state == RegisterForm.house_number.state:
        await state.update_data(street=data.get('reply_info'))
        await state.set_state(RegisterForm.flat_number)
        text = ua_config.get('registration', 'enter_flat_number')
    elif current_state == RegisterForm.flat_number.state:
        data = await state.get_data()
        try:
            date_to_save = datetime.strptime(data.get('birthday_date', ''), '%d.%m.%Y')
        except ValueError as e:
            date_to_save = None
        with session() as s:
            telegram_id = call.from_user.id
            user = s.query(User).filter(User.telegram_id == telegram_id).first()
            user.phone_number = data.get('phone_number')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.region = data.get('region')
            user.city = data.get('city')
            user.street = data.get('street')
            user.house_number = data.get('house_number')
            user.flat_number = data.get('flat_number')
            user.birthday_date = date_to_save
            s.add(user)
            s.commit()
        text = ua_config.get('registration', 'registration_complete')
        reply_markup = None

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


@main_router.callback_query(F.data == 'try_again')
async def process_try_again_callback(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    text = ''
    if current_state == RegisterForm.first_name.state:
        text = ua_config.get('registration', 'enter_first_name')
    elif current_state == RegisterForm.last_name.state:
        text = ua_config.get('registration', 'enter_last_name')
    elif current_state == RegisterForm.birthday_date.state:
        text = ua_config.get('registration', 'enter_birthday_date')
    elif current_state == RegisterForm.region.state:
        text = ua_config.get('registration', 'enter_region')
    elif current_state == RegisterForm.city.state:
        text = ua_config.get('registration', 'enter_city')
    elif current_state == RegisterForm.street.state:
        text = ua_config.get('registration', 'enter_street')
    elif current_state == RegisterForm.house_number.state:
        text = ua_config.get('registration', 'enter_house_number')
    elif current_state == RegisterForm.flat_number.state:
        text = ua_config.get('registration', 'enter_flat_number')

    await call.message.edit_reply_markup(reply_markup=None)
    await call.bot.edit_message_text(message_id=call.message.message_id,
                                     chat_id=call.message.chat.id,
                                     text=text)
