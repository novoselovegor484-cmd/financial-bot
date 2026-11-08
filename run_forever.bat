@echo off
chcp 65001 > nul
title FinancialOffersBot
cd /d "C:\Users\Администратор\Desktop\financial_offers_bot"

:loop
echo [%date% %time%] Запуск бота...
python bot.py
echo [%date% %time%] Бот завершил работу. Автоперезапуск через 5 сек...
timeout /t 5 /nobreak > nul
goto loop
