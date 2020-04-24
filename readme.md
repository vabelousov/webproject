# Up-the-hills #

## Разворачивание ##

### Шаг 1 - подготовка ###
      mkdir myproject; cd myproject  #  создаем папку проекта и заходим в нее
      git clone https://github.com/vabelousov/webproject.git  #  скачать проект с репозитория
      установить vrtualenv если не стоит: brew install virtualenv
### Шаг 2 - инициализация среды и установка пакетов ###
      virtualenv venv  #  инициализировать среду
      source venv/bin/activate  #  активация среды
      cd webproject
      pip install -r requirements.txt  #  установить пакеты
### Шаг 3 - создание миграций ###
      find . -path "*/migrations/*.py" -not -name "__init__.py" -delete find . -path "*/migrations/*.pyc" -delete
      rm db.sqlite3
      python manage.py makemigrations  #  создание миграций
      python manage.py migrate  #  выполнение миграций
### Шаг 4 - создание суперпользователя ###
      python manage.py createsuperuser  #  создание суперпользователя
### Готово ###
      python manage.py runserver