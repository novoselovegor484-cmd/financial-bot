# 🏦 Financial Offers Bot — Telegram-витрина финансовых офферов

## Быстрый старт

### 1. Установите зависимости
```bash
pip install -r requirements.txt
```

### 2. Получите токен бота
- Откройте [@BotFather](https://t.me/BotFather) в Telegram
- Отправьте `/newbot` и следуйте инструкциям
- Скопируйте токен (вида `123456:ABC-DEF...`)

### 3. Вставьте токен
Откройте файл **`.env`** и замените `ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА` на ваш токен:
```
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### 4. Запустите бота
```bash
python bot.py
```

### 5. Проверьте
Найдите вашего бота в Telegram и отправьте `/start` 🎉

---

## Как добавлять/редактировать офферы

Откройте файл **`offers.json`** и добавьте новый оффер в нужную категорию:

```json
{
  "id": "unique_id",
  "title": "Название продукта",
  "image_url": "https://ссылка-на-баннер.png",
  "rate": "от 10 % годовых",
  "limit": "до 500 000 ₽",
  "grace_period": "55 дней",
  "cashback": "до 5 %",
  "ref_link": "https://ваша-реферальная-ссылка"
}
```

> ⚠️ После изменения `offers.json` **перезапустите бота** (Ctrl+C → `python bot.py`)

---

## Как добавить новую категорию

Например, чтобы добавить **ОСАГО**:

1. В `offers.json` добавьте новый ключ:
   ```json
   "osago": [ { ...оффер... } ]
   ```

2. В `keyboards/main_menu.py` добавьте кнопку:
   ```python
   [InlineKeyboardButton(text="🚗 ОСАГО", callback_data="cat:osago")]
   ```

3. В `handlers/categories.py` добавьте маппинг:
   ```python
   "osago": "🚗 ОСАГО",
   ```

---

## Структура проекта

```
financial_offers_bot/
├── .env                    ← токен бота (НЕ коммитьте в git!)
├── bot.py                  ← точка входа
├── config.py               ← загрузка настроек
├── offers.json             ← база офферов (легко редактировать)
├── requirements.txt        ← зависимости
├── handlers/
│   ├── start.py            ← /start и приветствие
│   └── categories.py       ← показ офферов + пагинация
├── keyboards/
│   ├── main_menu.py        ← кнопки главного меню
│   └── offer_nav.py        ← кнопки навигации по офферам
└── models/
    └── offer.py            ← модель данных оффера
```
