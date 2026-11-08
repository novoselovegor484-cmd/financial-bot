# models/offer.py — Pydantic-модель оффера
from pydantic import BaseModel


class Offer(BaseModel):
    """Один финансовый оффер.

    Поля:
        id          — уникальный идентификатор (для callback_data)
        title       — название продукта (банк / МФО)
        image_url   — прямая ссылка на баннер-картинку
        rate        — процентная ставка / условия
        limit       — лимит суммы
        grace_period— льготный период
        cashback    — размер кешбэка
        ref_link    — ваша реферальная (партнёрская) ссылка
    """
    id: str
    title: str
    image_url: str
    rate: str
    limit: str
    grace_period: str
    cashback: str
    ref_link: str
