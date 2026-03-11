@echo off
echo Starting Warsaw Rentals ETL Pipeline...

:: 1. Переходимо в папку з проєктом (ЗАМІНИ НА СВІЙ РЕАЛЬНИЙ ШЛЯХ!)
cd /d "C:\Users\Admin\Documents\pl_real_estate"

:: 2. Активуємо віртуальне середовище
call venv\Scripts\activate

:: 3. Запускаємо скрипти по черзі
echo Running Scraper...
python scraper.py

echo Running Cleaner...
python clean_data.py

echo Loading to PostgreSQL...
python load_to_postgres.py

:: 4. Деактивуємо середовище
deactivate

echo Pipeline finished successfully!
:: pause (можеш розкоментувати слово pause, щоб вікно терміналу не закривалося одразу і ти міг прочитати логи)