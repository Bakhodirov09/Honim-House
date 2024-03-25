from aiogram import executor
from main.database_set import database
from loader import dp
import middlewares, filters, handlers
from utils.db_api.database_settings import get_menu
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await database.connect()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    await database.disconnect()
    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
