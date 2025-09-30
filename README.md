# Локальный сервис просмотра аналитики по проектам
Структура:
- index.html — каталог проектов (SPA)
- reports.json — реестр отчётов
- projects/<PROJECT_ID>/ — папка проекта с HTML-отчётами и их файловой обвязкой (картинки, скрипты)
- tools/build_reports_json.py — сканер, пересобирающий reports.json

Запуск:
1) Откройте терминал в папке analytics_catalog/
2) python -m http.server 8000
3) Браузер: http://localhost:8000/index.html

Добавление проекта: создайте projects/0006_ABC/, положите туда отчёт(ы), запустите python tools/build_reports_json.py
