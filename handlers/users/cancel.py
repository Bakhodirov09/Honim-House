from aiogram.dispatcher import FSMContext

from keyboards.default.default_keyboards import admins_panel, users_menu_uz, users_menu_ru
from loader import dp, types
from utils.db_api.database_settings import is_admin, get_user


@dp.message_handler(state="*", text=f"❌ Bekor qilish")
async def cancel_handler(message: types.Message, state: FSMContext):
    userga = f"❌ Bekor qilindi"
    if await is_admin(chat_id=message.chat.id):
        await message.answer(text=userga, reply_markup=admins_panel)
    else:
        await message.answer(text=userga, reply_markup=users_menu_uz)
    await state.finish()

@dp.message_handler(state="*", text=f"❌ Отмена")
async def cancel_ru_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=users_menu_ru)
    await state.finish()


@dp.callback_query_handler(state='*', text=f"back_main_menu_uz")
async def back_main_menu_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if await is_admin(chat_id=call.message.chat.id):
        await call.message.answer(text=f"❌ Bekor qilindi", reply_markup=admins_panel)
    else:
        await call.message.answer(text=f"❌ Bekor qilindi", reply_markup=users_menu_uz)
    await state.finish()

@dp.callback_query_handler(state='*', text=f"back_main_menu_ru")
async def back_main_menu_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=f"❌ Отменено", reply_markup=users_menu_ru)
    await state.finish()

@dp.message_handler(state='*' ,text=f"🏘 Главное меню")
async def back_main_menu_ru(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=users_menu_ru)
    await state.finish()

@dp.message_handler(state='*' ,text=f"🏘 Asosiy menyu")
async def back_main_menu_ru(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=users_menu_uz)
    await state.finish()
