#!/bin/bash
set -e

echo "=== Установка Telegram Бота ==="

# Обновление пакетов и установка Python
apt-get update
apt-get install -y python3 python3-pip python3-venv git

# Переход в директорию
APP_DIR="/opt/financial_offers_bot"
mkdir -p "$APP_DIR"
cp -r . "$APP_DIR"
cd "$APP_DIR"

# Настройка виртуального окружения
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Создание systemd сервиса для автозапуска 24/7
cat <<EOF > /etc/systemd/system/financial_bot.service
[Unit]
Description=Financial Offers Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Запуск и включение автозапуска
systemctl daemon-reload
systemctl enable financial_bot
systemctl restart financial_bot

echo "=== Бот успешно запущен и работает 24/7! ==="
systemctl status financial_bot --no-pager
