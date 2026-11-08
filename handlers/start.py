# handlers/start.py — Команда /start и приветствие
from html import escape
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Приветственное сообщение + главное меню."""
    raw_name = message.from_user.full_name if message.from_user else "друг"
    name = escape(raw_name)
    text = (
        f"👋 Привет, <b>{name}</b>!\n\n"
        "Я — твой финансовый помощник.\n"
        "Помогу подобрать лучшие предложения:\n"
        "микрозаймы, дебетовые и кредитные карты.\n\n"
        "👇 <b>Выбери категорию:</b>"
    )
    await message.answer(text, reply_markup=main_menu_kb())
