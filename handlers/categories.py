# handlers/categories.py — Вывод офферов и навигация по страницам
import json
import logging
from html import escape
from pathlib import Path
from typing import Dict, List, Optional

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InputMediaPhoto,
    URLInputFile,
)

from config import SHOWCASE_URL
from models.offer import Offer
from keyboards.offer_nav import build_offer_kb
from keyboards.main_menu import main_menu_kb

logger = logging.getLogger(__name__)
router = Router()

# ══════════════════════════════════════════════════════════════════
#  Маппинг коротких ключей ➜ человеко-читаемых заголовков
# ══════════════════════════════════════════════════════════════════
CATEGORY_MAP: Dict[str, str] = {
    "mfo":    "💸 Микрозаймы (МФО)",
    "debit":  "💳 Дебетовые карты",
    "credit": "💳 Кредитные карты",
}

OFFERS_PATH = Path(__file__).resolve().parent.parent / "offers.json"


def load_offers() -> Dict[str, List[Offer]]:
    """Читает offers.json на каждый запрос для актуальности данных."""
    try:
        raw = json.loads(OFFERS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.error("offers.json не найден по пути %s", OFFERS_PATH)
        return {}
    except json.JSONDecodeError as exc:
        logger.error("Ошибка JSON в offers.json: %s", exc)
        return {}

    result: Dict[str, List[Offer]] = {}
    for cat_key, items in raw.items():
        result[cat_key] = [Offer(**item) for item in items]
    return result


def _format_caption(offer: Offer, idx: int, total: int, cat_label: str, cat_key: str = "") -> str:
    """Красивый HTML-текст для карточки оффера."""
    lines = [
        f"<b>{escape(cat_label)}</b>  ·  {idx + 1} из {total}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"\n🏦 <b>{escape(offer.title)}</b>\n",
    ]

    if offer.rate and offer.rate.strip() and offer.rate.strip() != "—":
        lines.append(f"📊 <b>Ставка:</b>  {escape(offer.rate.strip())}")
    if offer.limit and offer.limit.strip() and offer.limit.strip() != "—":
        lines.append(f"💰 <b>Сумма:</b>  {escape(offer.limit.strip())}")
    if offer.grace_period and offer.grace_period.strip() and offer.grace_period.strip() != "—":
        lines.append(f"⏳ <b>Срок:</b>  {escape(offer.grace_period.strip())}")
    if offer.cashback and offer.cashback.strip() and offer.cashback.strip() != "—":
        lines.append(f"👤 <b>Требования:</b>  {escape(offer.cashback.strip())}")

    # Во вкладке микрозаймов аккуратно подсвечиваем переход на полную онлайн-витрину
    if cat_key == "mfo":
        lines.append(
            f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>Нужно больше вариантов?</b>\n"
            f"👉 <a href=\"{SHOWCASE_URL}\"><b>Онлайн-витрина займов (50+ МФО)</b></a>"
        )

    return "\n".join(lines)


def _has_valid_image(image_url: Optional[str]) -> bool:
    """Проверяет, указана ли реальная ссылка на картинку."""
    url = (image_url or "").strip()
    return url.startswith("http://") or url.startswith("https://")


# ══════════════════════════════════════════════════════════════════
#  CALLBACK-ОБРАБОТЧИКИ
# ══════════════════════════════════════════════════════════════════


@router.callback_query(F.data.startswith("cat:"))
async def show_category(callback: CallbackQuery) -> None:
    """Пользователь выбрал категорию — показываем первый оффер."""
    cat_key = callback.data.split(":", 1)[1]
    cat_label = CATEGORY_MAP.get(cat_key, cat_key)
    offers = load_offers().get(cat_key, [])

    if not offers:
        await callback.answer(
            "😔 В этой категории пока нет активных предложений.",
            show_alert=True,
        )
        return

    offer = offers[0]
    caption = _format_caption(offer, 0, len(offers), cat_label, cat_key=cat_key)
    kb = build_offer_kb(cat_key, 0, len(offers), offer.ref_link)

    # Если есть картинка — отправляем фото, иначе текстовое сообщение
    if _has_valid_image(offer.image_url):
        try:
            await callback.message.answer_photo(
                photo=URLInputFile(offer.image_url.strip(), filename=f"{offer.id}.png"),
                caption=caption,
                reply_markup=kb,
            )
            await callback.answer()
            return
        except Exception as exc:
            logger.warning("Не удалось отправить фото (%s), отправляем текстом: %s", offer.image_url, exc)

    # Запасной или основной текстовый вариант
    await callback.message.answer(text=caption, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("nav:"))
async def navigate_offer(callback: CallbackQuery) -> None:
    """Пользователь нажал ◀️ Назад / Вперёд ▶️ — листаем офферы."""
    parts = callback.data.split(":")
    cat_key = parts[1]
    page = int(parts[2])

    cat_label = CATEGORY_MAP.get(cat_key, cat_key)
    offers = load_offers().get(cat_key, [])

    if not offers or page < 0 or page >= len(offers):
        await callback.answer("⚠️ Оффер не найден.", show_alert=True)
        return

    offer = offers[page]
    caption = _format_caption(offer, page, len(offers), cat_label, cat_key=cat_key)
    kb = build_offer_kb(cat_key, page, len(offers), offer.ref_link)

    current_is_photo = bool(callback.message.photo)
    next_has_photo = _has_valid_image(offer.image_url)

    # Сценарий 1: было фото и следующее фото — редактируем медиа
    if current_is_photo and next_has_photo:
        try:
            media = InputMediaPhoto(
                media=URLInputFile(offer.image_url.strip(), filename=f"{offer.id}.png"),
                caption=caption,
            )
            await callback.message.edit_media(media=media, reply_markup=kb)
            await callback.answer()
            return
        except Exception as exc:
            logger.warning("edit_media failed: %s", exc)

    # Сценарий 2: был текст и следующий текст — просто редактируем текст
    if not current_is_photo and not next_has_photo:
        try:
            await callback.message.edit_text(text=caption, reply_markup=kb)
            await callback.answer()
            return
        except Exception as exc:
            logger.warning("edit_text failed: %s", exc)

    # Сценарий 3: переключение между фото и текстом (или ошибка редактирования)
    try:
        await callback.message.delete()
    except Exception:
        pass

    if next_has_photo:
        try:
            await callback.message.answer_photo(
                photo=URLInputFile(offer.image_url.strip(), filename=f"{offer.id}.png"),
                caption=caption,
                reply_markup=kb,
            )
            await callback.answer()
            return
        except Exception as exc:
            logger.warning("answer_photo fallback: %s", exc)

    await callback.message.answer(text=caption, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "no_ref_link")
async def no_ref_link_handler(callback: CallbackQuery) -> None:
    """Уведомление, если ссылка на оффер ещё настраивается."""
    await callback.answer("⚙️ Ссылка на этот оффер сейчас обновляется.", show_alert=True)


@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery) -> None:
    """Возврат в главное меню."""
    await callback.message.answer(
        "📋 <b>Главное меню</b>\n\nВыберите категорию:",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery) -> None:
    """Пустой коллбек для кнопки-счётчика страниц."""
    await callback.answer()
