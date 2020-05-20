# Up-the-hills #

## Разворачивание ##

### Шаг 1 - подготовка ###
      brew doctor; brew update; brew install postgresql  #  установка базы данных PostgreSQL
      brew install gettext  #  установка GNU gettext для интернационализации
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
### Переводы ###
      mkdir locale  #  в корне проекта (там где manage.py) нужно сделать папку locale
      python manage.py makemessages -l ru;  #  стартуя с чистого листа - нужно сгенерить файлы переводов
      python manage.py makemessages -l en;
      python manage.py makemessages -l fr;
      редактируем переводы в locale/ru/LC_MESSAGES/django.po
      python manage.py compilemessages  #  компилируем переводы
      python manage.py makemessages -a  #  если что то изменилось в коде или шаблонах - обновляем
      Для переводов моделей, ничего делать не нужно - переводы делаем в админке, но если вдруг
      появилась новая модель для перевода на уже работающей базе - но нужно выполнить команду
      ниже, которая добавит поля в таблицы переводов модели.
      python manage.py update_translation_fields

### экспорт импорт дампа ###
      python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
      scp db.json юзер@хост:~/путь/
      python manage.py loaddata db.json
      