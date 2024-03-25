from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import types
from utils.db_api.database_settings import get_user
from keyboards.default.default_keyboards import users_menu_uz, users_menu_ru

class CheckDate(BaseMiddleware):
    async def pre_process(self, update: types.Update):
        if update.message:
            if update.message.date[12:13] >= 9 and update.message.date[12:13] < 21:
                return
            else:
                user = await get_user(chat_id=update.message.chat.id)
                if user:
                    if user[3] == "uz":
                        await update.message.answer(text=f"😕 Kechirasiz ish vaqtimiz: 09:00 dan 21:00 gacha",
                                                    reply_markup=users_menu_uz)
                    else:
                        await update.message.answer(text=f"😕 Извините, мы работаем с 09:00 до 21:00.", reply_markup=users_menu_ru)
                else:
                    if update.message.from_user.language_code == "uz":
                        await update.message.answer(text=f"😕 Kechirasiz ish vaqtimiz: 09:00 dan 21:00 gacha")
                    else:
                        await update.message.answer(text=f"😕 Извините, мы работаем с 09:00 до 21:00.")

                raise CancelHandler()
        elif update.callback_query:
            if update.callback_query.message.date[12:13] >= 9 and update.callback_query.message.date[12:13] < 21:
                return
            else:
                user = await get_user(chat_id=update.callback_query.message.chat.id)
                if user:
                    if user[3] == "uz":
                        await update.callback_query.message.answer(
                            text=f"😕 Kechirasiz ish vaqtimiz: 09:00 dan 21:00 gacha", reply_markup=users_menu_uz)
                    else:
                        await update.callback_query.message.answer(text=f"😕 Извините, мы работаем с 09:00 до 21:00.",
                                                                   reply_markup=users_menu_ru)
                else:
                    if update.callback_query.message.from_user.language_code == "uz":
                        await update.message.answer(text=f"😕 Kechirasiz ish vaqtimiz: 09:00 dan 21:00 gacha")
                    else:
                        await update.callback_query.message.answer(text=f"😕 Извините, мы работаем с 09:00 до 21:00.")
                raise CancelHandler()