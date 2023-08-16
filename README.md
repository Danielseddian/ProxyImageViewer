# ProxyImageViewer
## Django проект по проксированию изображений с лимитом выдачи результатов. 

# Настройка и запуск:
## Перед началом работы потребуется python 3.10+, а также рекомендуется создать изолированное виртуальное окружение:
### Для linux:
```bash
python3 -m venv venv
```
### Для Windows:
```bash
python -m venv venv
```
## После этого необходимо установить зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```
## После установки всех зависимостей необходимо создать файл config.ini в корневом каталоге проекта. Для удобства можно переименовать файл config.ini.example и внести необходимые изменения:
```bash
mv config.ini.example config.ini
```
## Для правильной работы проекта необходимо применить миграции:
```bash
python manage.py migrate
```
## А также рекомендуется создать суперпользователя (выполнить команду и следовать инструкциям):
```bash
python manage.py createsuperuser
```
## Для запуска можно воспользоваться командой:
```bash
python manage.py runserver
```
## После этого проект будет доступен по адресу:
- http://localhots:8000/
## Также можно загрузить данные для проксирования изображений в формате .csv (потребуются права суперпользователя):
- http://localhots:8000/upload/