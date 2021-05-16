python3 -m venv env - инициализация виртуального окружения

Активация окружения

*Unix:

source env/bin/activate

Windows:

cd env/Scripts

activate

pip install -r requirements.txt - установка зависимостей

docker-compose up - поднятие базы данных

python src/manage.py migrate - запуск миграций

python src/manage.py runserver - запуск приложения