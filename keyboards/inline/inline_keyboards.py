from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('🇺🇿 Uzbek tili', callback_data='uz'),
            InlineKeyboardButton('🇷🇺 Русский Язык', callback_data='ru')
        ]
    ]
)

async def plus_minus_def(now, price, basket, basket_data, back, back_data):
    plus_minus = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"➖", callback_data='minus'),
                InlineKeyboardButton(text=f"{now} / {price}", callback_data='information'),
                InlineKeyboardButton(text=f"➕", callback_data='plus')
            ],
            [
                InlineKeyboardButton(text=f"{basket}", callback_data=f'{basket_data}')
            ],
            [
                InlineKeyboardButton(text=f"{back}", callback_data=f'{back_data}')
            ]
        ]
    )
    return plus_minus
