# Up-the-hills #

## Разворачивание ##

### Шаг 1 - подготовка ###
      brew doctor; brew update; brew install postgresql  #  установка базы данных PostgreSQL
      mkdir myproject; cd myproject  #  создаем папку проекта и заходим в нее
      git clone https://github.com/vabelousov/webproject.git  #  скачать проект с репозитория
      установить vrtualenv если не стоит: brew install virtualenv
### Шаг 2 - инициализация среды и установка пакетов ###
      virtualenv venv  #  инициализировать среду
      source venv/bin/activate  #  активация среды
      cd webproject
      pip install -r requirements.txt  #  установить пакеты
### Шаг 3 - создание БД
      createuser -dP webproject
      createdb -E utf8 -U webproject webproject
### Шаг 4 - создание миграций ###
      python manage.py makemigrations  #  создание миграций (если необходимо)
      python manage.py migrate  #  выполнение миграций
### Шаг 5 - создание суперпользователя ###
      python manage.py createsuperuser  #  создание суперпользователя
### Готово ###
      python manage.py runserver  #  запуск сервера
      http://localhost:8000/  #  открытие сайта