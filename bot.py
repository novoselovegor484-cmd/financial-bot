# bot.py — Точка входа: запуск Telegram-бота
import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
from aiogram.types import ErrorEvent

from config import BOT_TOKEN, PROXY_URL
from handlers.start import router as start_router
from handlers.categories import router as categories_router

# ── Настройка логирования ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

RETRY_DELAY = 10
MAX_RETRIES = 20


def build_session() -> AiohttpSession:
    """Создаёт сессию для бота (с прокси, если задан PROXY_URL в .env)."""
    if PROXY_URL:
        logger.info("Используется прокси: %s", PROXY_URL)
        return AiohttpSession(proxy=PROXY_URL)
    return AiohttpSession()


async def start_healthcheck_server(port: int) -> web.AppRunner:
    """
    Запуск простого веб-сервера для облачных платформ (Render, Koyeb и др.).
    Позволяет платформе видеть, что сервис жив (Healthcheck),
    а также держать бота активным 24/7 через пинг (UptimeRobot).
    """
    async def ping(_request: web.Request) -> web.Response:
        return web.Response(text="Bot is running 24/7!", content_type="text/plain")

    app = web.Application()
    app.router.add_get("/", ping)
    app.router.add_get("/health", ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Веб-сервер проверки здоровья запущен на порту %d", port)
    return runner


async def main() -> None:
    # ── Запуск веб-сервера для Render (если задана переменная PORT) ──
    web_runner = None
    port_env = os.getenv("PORT")
    if port_env:
        try:
            port = int(port_env)
            web_runner = await start_healthcheck_server(port)
        except Exception as e:
            logger.warning("Не удалось запустить веб-сервер: %s", e)

    session = build_session()
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(categories_router)

    @dp.error()
    async def on_error(event: ErrorEvent) -> None:
        logger.error("Необработанная ошибка: %r", event.exception, exc_info=True)
        if event.update and event.update.callback_query:
            try:
                await event.update.callback_query.answer(
                    "Произошла ошибка. Попробуйте ещё раз.",
                    show_alert=True,
                )
            except Exception:
                pass

    # ── Запуск polling с авто-повтором при сетевой ошибке ────────
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Попытка %d/%d: подключаемся к Telegram...", attempt, MAX_RETRIES)
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Бот запущен! Polling активен.")
            await dp.start_polling(bot)
            break
        except TelegramNetworkError as e:
            logger.warning("Сетевая ошибка (%s). Повтор через %d сек...", e, RETRY_DELAY)
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)
        except KeyboardInterrupt:
            logger.info("Бот остановлен вручную.")
            break
        except Exception as e:
            logger.error("Неожиданная ошибка: %r", e, exc_info=True)
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)

    if web_runner:
        await web_runner.cleanup()
    await bot.session.close()
    logger.info("Сессия закрыта.")


if __name__ == "__main__":
    asyncio.run(main())
