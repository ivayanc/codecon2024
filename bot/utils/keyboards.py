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
                    KeyboardButton(text=ua_config.get('main_menu', 'ask_volunteer_help')),
                    KeyboardButton(text=ua_config.get('main_menu', 'ask_government_help'))
                ],
                [
                    KeyboardButton(text=ua_config.get('main_menu', 'request_evacuation'))
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

    @staticmethod
    def region_keyboard(regions: list[tuple]):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for region_id, region_name in regions:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text=region_name, callback_data=str(region_id))
            ])
        return keyboard

    @staticmethod
    def yes_no_keyboard():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=ua_config.get('yes_no', 'yes'), callback_data='yes'),
                    InlineKeyboardButton(text=ua_config.get('yes_no', 'no'), callback_data='no'),
                ]
            ],
        )
        return keyboard


class EvacuationKeyboards:
    @staticmethod
    def evacuation_for_who():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=ua_config.get('evacuation_prompts', 'for_me'),
                                     callback_data='evacuation_for_me'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('evacuation_prompts', 'for_other'),
                                     callback_data='evacuation_for_other'),
            ]
        ])
        return keyboard


class RequestKeyboards:

    @staticmethod
    def select_type(types: list[str]):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for type in types:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text=type, callback_data=type)
            ])
        return keyboard

    @staticmethod
    def select_delivery_type():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=ua_config.get('request_prompts', 'pickup'), callback_data='pickup'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('request_prompts', 'delivery'), callback_data='delivery'),
            ]
        ])
        return keyboard

    @staticmethod
    def request_for_who():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=ua_config.get('request_prompts', 'for_me'),
                                     callback_data='request_for_me'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('request_prompts', 'for_other'),
                                     callback_data='request_for_other'),
            ]
        ])
        return keyboard
