from aiogram import types

from keyboards.default.default_keyboards import users_menu_uz, users_menu_ru
from loader import dp
from utils.db_api.database_settings import get_user


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    user = await get_user(chat_id=message.chat.id)
    if user[3] == "uz":
        await message.answer(text=f"Xush kelibsiz", reply_markup=users_menu_uz)
    else:
        await message.answer(text=f"Добро пожаловать", reply_markup=users_menu_ru)