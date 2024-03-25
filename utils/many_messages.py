from aiogram import types
from keyboards.default.default_keyboards import users_menu_uz, admins_panel, users_menu_ru
from loader import dp
from utils.db_api.database_settings import is_admin, get_user
from aiogram.dispatcher import FSMContext

async def send_message_to_user(message: types.Message):
    await message.answer(text=f"😕 Kechirasiz siz adminlik huquqiiga ega emassiz bu funksiya faqat adminlar uchun!",
                         reply_markup=users_menu_uz)


async def error(message: types.Message):
    userga = f"404 function not found"
    if await is_admin(chat_id=message.chat.id):
        await message.answer(text=userga, reply_markup=admins_panel)
    else:
        user = await get_user(chat_id=message.chat.id)
        if user:
            if user[3] == "uz":
                await message.answer(text=userga, reply_markup=users_menu_uz)
            else:
                await message.answer(text=userga, reply_markup=users_menu_ru)
        else:
            await message.answer(text=userga)



async def send_error(e):
    await dp.bot.send_message(chat_id=-1002075245072, text=f"Error:\n\n<b>{e}</b>\n\nBot: <b>Honim House</b>")
