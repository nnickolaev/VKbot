# Чат-бот для VK


## VKinder
Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок.

Используя данные из VK, нужно сделать сервис намного лучше, чем Tinder, а именно: чат-бота "VKinder". 
Бот должен искать людей, подходящих под условия, на основании информации о пользователе из VK:
- возраст,
- пол,
- город,
- семейное положение.

У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии профиля и отправлять их пользователю в чат вместе со ссылкой на найденного человека.  
Популярность определяется по количеству лайков и комментариев.
 
Как настроить группу и получить токен можно найти в [инструкции](group_settings.md)  

## Описание файлов:
1. Модуль работы с бэкэндом VK [core.py](core.py)
2. Модуль работы с Базой данных [database.py](database.py)
3. Модуль работы с фронтэндом бота [interface.py](interface.py)
4. Модуль запуска бота VKinder [main.py](main.py)
5. Модуль конфигураций [config.py](config.py)
6. Перечень необходимых пакетов [requirements.txt](requirements.txt)

## Перечень команд бота:
- Привет - для начала работы
- Поиск - начать поиск подходящих профилей
- Далее - получить следующий профиль
- Сброс - сброс просмотренных профилей 
- Помощь - получить список команд
- Пока - прощание с ботом
