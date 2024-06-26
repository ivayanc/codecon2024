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

    @staticmethod
    def evacuation_rate_keyboard(request_id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate1'),
                                         callback_data=f'selectevacuationrate_{request_id}_1'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate2'),
                                         callback_data=f'selectevacuationrate_{request_id}_2'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate3'),
                                         callback_data=f'selectevacuationrate_{request_id}_3'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate4'),
                                         callback_data=f'selectevacuationrate_{request_id}_4'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate5'),
                                         callback_data=f'selectevacuationrate_{request_id}_5'),
                ]
            ],
        )
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

    @staticmethod
    def request_rate_keyboard(request_id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate1'),
                                         callback_data=f'selectrequestrate_{request_id}_1'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate2'),
                                         callback_data=f'selectrequestrate_{request_id}_2'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate3'),
                                         callback_data=f'selectrequestrate_{request_id}_3'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate4'),
                                         callback_data=f'selectrequestrate_{request_id}_4'),
                    InlineKeyboardButton(text=ua_config.get('ratings', 'rate5'),
                                         callback_data=f'selectrequestrate_{request_id}_5'),
                ]
            ],
        )
        return keyboard


class GovernmentHelpKeyboards:
    @staticmethod
    def main_inline_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=ua_config.get('government_help', 'first_option'), callback_data='first_option'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('government_help', 'second_option'),
                                     callback_data='second_option'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('government_help', 'third_option'),
                                     callback_data='third_option'),
            ],
            [
                InlineKeyboardButton(text=ua_config.get('government_help', 'fourth_option'),
                                     callback_data='fourth_option'),
            ]
        ])
        return keyboard
