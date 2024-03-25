from aiogram.dispatcher import FSMContext

from keyboards.default.default_keyboards import users_menu_uz
from loader import dp, types
from utils.db_api.database_settings import curers_settings, basket_settings, orders_settings, get_user
from utils.many_messages import error


@dp.callback_query_handler()
async def ordered_bttn_handler(call: types.CallbackQuery, state: FSMContext):
    if await curers_settings(work='get', chat_id=call.message.chat.id):
        order = call.data.split('_')
        await orders_settings(work='update', number=int(order[2]))
        await call.message.answer(text=f"✅", reply_markup=users_menu_uz)
        await state.finish()
    else:
        await error(call.message, d)
        await state.finish()