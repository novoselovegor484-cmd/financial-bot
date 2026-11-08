# config.py — загрузка настроек из .env
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ── Токен бота ────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN or BOT_TOKEN == "ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА":
    raise RuntimeError(
        "❌ BOT_TOKEN не найден!\n"
        "   Откройте файл .env и добавьте: BOT_TOKEN=ваш_токен"
    )

# ── Ссылка на витрину займов ──────────────────────────────────────
SHOWCASE_URL: str = os.getenv(
    "SHOWCASE_URL",
    "https://zaimstore.com/6af0613b2c6cb"
)

# ── SOCKS5-прокси (опционально) ───────────────────────────────────
# Задайте в .env: PROXY_URL=socks5://host:port
# Или с авторизацией: PROXY_URL=socks5://user:pass@host:port
PROXY_URL: str = os.getenv("PROXY_URL", "")
