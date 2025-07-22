Стек: DRF, PostgreSQL, Gunicorn, faker для генерации названий заголовков к видео, drf-spectacular для автодокументации 

Запуск проекта:

Клонируйте репозиторий:

```bash
git clone https://github.com/your-repo/likes.git
```

Собрать и запустить проект, команды выполнить из корневой директории:

```bash
docker-compose up --build
```

При сборке и запуске миграция применится автоматически, если этого не произошло:

```bash
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```


Наполнить БД: 

```bash
docker-compose exec web python manage.py generate_test_d
```

При выполнении этой команды создастся 10000 пользователей, 100000 видео-новостей, ~200000 видео-файлов.


Приложение будет доступно по адресу:
http://localhost:8000/

Swagger-схема: 
http://localhost:8000/api/swagger/

Реализованные ендпоинты:

GET	/v1/videos/	Список всех видео

GET	/v1/videos/{id}/ Детали видео

POST /v1/videos/{id}/likes/	Поставить лайк

DELETE /v1/videos/{id}/likes/	Удалить лайк

GET	/v1/videos/ids/	ID всех опубликованных видео (только для staff)

GET	/v1/videos/statistics-group-by/	Статистика через GROUP BY

GET	/v1/videos/statistics-subquery/	Статистика через подзапросы

Конкурентность обеспечивается атомарными транзакциями с select_for_update.
