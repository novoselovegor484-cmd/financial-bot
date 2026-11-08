# keyboards/main_menu.py — Клавиатура главного меню
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура с категориями офферов."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💸 Микрозаймы (МФО)",
            callback_data="cat:mfo",
        )],
        [InlineKeyboardButton(
            text="💳 Дебетовые карты",
            callback_data="cat:debit",
        )],
        [InlineKeyboardButton(
            text="💳 Кредитные карты",
            callback_data="cat:credit",
        )],
    ])
