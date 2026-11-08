@echo off
chcp 65001 > nul
echo Остановка бота...
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*bot.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Бот остановлен.
timeout /t 3 > nul
