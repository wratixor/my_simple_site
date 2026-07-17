#!/bin/bash
set -e
cd /var/www/wratixor.ru/my_simple_site

# Получаем последние изменения из Gitea
git fetch gitea master
git reset --hard gitea/master
git clean -fd

# Активируем виртуальное окружение
source .venv/bin/activate

# Устанавливаем/обновляем зависимости
pip install -r requirements.txt

# Применяем миграции (если есть)
# python manage.py migrate  # для Wagtail или другие скрипты

# Перезапускаем службу
sudo systemctl restart site.service

echo "Deployment completed at $(date)"