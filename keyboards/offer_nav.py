# keyboards/offer_nav.py — Навигация по офферам (пагинация)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SHOWCASE_URL


def build_offer_kb(
    cat_key: str,
    current: int,
    total: int,
    ref_link: str,
) -> InlineKeyboardMarkup:
    """Кнопки под карточкой оффера: Оформить + Витрина (для МФО) + ◀️ 1/N ▶️ + Меню."""
    rows: list[list[InlineKeyboardButton]] = []

    # ── Ряд 1: кнопка «Оформить заявку» ──
    link = (ref_link or "").strip()
    if link.startswith("http://") or link.startswith("https://"):
        rows.append([
            InlineKeyboardButton(text="📝 Оформить заявку", url=link),
        ])
    else:
        rows.append([
            InlineKeyboardButton(text="📝 Оформить заявку", callback_data="no_ref_link"),
        ])

    # ── Ряд 2: кнопка витрины (высвечивается именно во вкладке микрозаймов) ──
    if cat_key == "mfo":
        rows.append([
            InlineKeyboardButton(
                text="🚀 Ещё больше займов (Витрина)",
                url=SHOWCASE_URL,
            ),
        ])

    # ── Ряд 3: навигация (если офферов больше одного) ──
    if total > 1:
        nav: list[InlineKeyboardButton] = []

        if current > 0:
            nav.append(InlineKeyboardButton(
                text="◀️ Назад",
                callback_data=f"nav:{cat_key}:{current - 1}",
            ))

        nav.append(InlineKeyboardButton(
            text=f"  {current + 1} / {total}  ",
            callback_data="noop",
        ))

        if current < total - 1:
            nav.append(InlineKeyboardButton(
                text="Вперёд ▶️",
                callback_data=f"nav:{cat_key}:{current + 1}",
            ))

        rows.append(nav)

    # ── Ряд 4: вернуться в главное меню ──
    rows.append([
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)
