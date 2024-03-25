from aiogram import Dispatcher

from loader import dp
from middlewares.middleware import CheckDate


if __name__ == "middlewares":
    dp.middleware.setup(CheckDate())
