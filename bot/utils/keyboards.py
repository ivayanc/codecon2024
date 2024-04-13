from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


from configuration import ua_config


class MainKeyboards:

    @staticmethod
    def default_keyboard():
        """
        :param: ignore_admin - if True returns user keyboard for Admins and SuperAdmins
        """
        return MainKeyboards.guest_keyboard()

    @staticmethod
    def guest_keyboard():
        result_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Тут буде меню')
                ]
            ],
            resize_keyboard=True
        )
        return result_kb

    @staticmethod
    def share_contact_keyboard():
        share_button = KeyboardButton(text=ua_config.get('buttons', 'share_contact'), request_contact=True)
        share_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    share_button
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        return share_keyboard

    @staticmethod
    def validate_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=ua_config.get('buttons', 'again'), callback_data='try_again'),
                InlineKeyboardButton(text=ua_config.get('buttons', 'validate'), callback_data='validate')
            ]
        ])
        return keyboard
