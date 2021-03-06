Проект "Green Atom TEST"
===========================


Общие требования
----------------
---

> > Для разработки требуется использовать Python версии 3.8 и выше.
> > Приложение должно функционировать в среде ОС Linux.
> > Требуется использовать библиотеку FastApi (https://fastapi.tiangolo.com).
> > В качестве базы данных следует использовать Postgres актуальной версии или
> > sqlite.
> > Требуется предоставить ссылку и доступ к репозиторию кода в облачном
> > хранилище.

Функциональное описание
-----------------------
---

| Название              | Метод  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Описание |
|-----------------------|:------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| /frames/              |  POST  | На вход подаются изображения в формате jpeg. Количество передаваемых файлов может быть от 1 до 15. Результат работы функции соответствует стандартному для HTTP коду. Функция сохраняет переданные файлы в корзину с именем <дата в формате YYYYMMDD> объектного хранилища min.io с именами <UUID>.jpg и фиксирует в базе данных в таблице inbox со структурой <код запроса>  <имя сохраненного файла>  <дата / время регистрации> Код запроса формируется автоматически. Метод возвращает перечень созданных элементов в формате JSON. |
| /frames/<код запроса> |  GET   |                                                                                                                                                                                                                                                                                                На вход подается код запроса. На выходе возвращается список соответствующих коду запроса изображений в формате JSON, включая дату и время регистрации и имена файлов. Результат работы функции соответствует стандартному для HTTP коду. |
| /frames/<код запроса> | DELETE |                                                                                                                                                                                                                                                                                                                          На вход подается код запроса. Функция удаляет данные по запросу из базы данных и соответствующие файлы изображений из объектного хранилища. Результат работы функции соответствует стандартному для HTTP коду. |

Основные технологии
-------------------
---

>>* Python 3.8
>>* FastAPI 0.78.0
>>* Postgresql 14.2
>>* Сервис min.io

>> * Docker
>> * Docker Compose


Установка и запуск
------------------
---

* Переходим в директорию

```
cd green_test
```

1. Создаем файл ".env" по примеру с файла .env.sample
* Для тестирования можно просто файл .evn.sample переименовать в .env



Запуск с помощью docker-compose
-------------------------------
---

~~~
docker-compose up --build
~~~

2. Переходим в браузере на наш min.io
Адрес появился в терминале (192.168.x.x:9001). Авторизуемся
login - minioadmin, password- minioadmin
Далее Identity -> Service Accounts -> Create service account
Нажимаем Create. Записываем в файл evn_min_io.py -> "ACCESS_KEY_MIN_IO=Access Key",
"SECRET_KEY_MIN_IO=Secret Key" и SERVER_MIN_IO=192.168.x.x (тот самый адрес, который появился в терминале). PORT_MIN_IO оставляем 9000

Запуск тестоов с помощью docker-compose
-------------------------------
---
~~~
docker-compose exec web pytest tests/tests_app.py 
~~~
