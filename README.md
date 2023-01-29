# API для выдачи меню ресторана
Содержит в себе роуты на меню, подменю и блюда.
В каждом меню может быть подменю, так же в каждом подменю может быть блюдо.
Подменю может принадлежать только к одному меню, а блюдо только к одному подменю.

---
## Запуск приложения
Перед запуском сервера необходимо наполнить .env-файл по аналогии с примером в репозитории

В папке `infra` скачанного репозитория выполните:
```
    docker-compose up -d # для запуска основного приложения
    docker-compose -f docker-compose.test.yml up -d # для запуска контейнера с тестами
```
 API будет доступен по адресу `localhost:8000`. Документация доступна по `localhost:8000/docs`.

 ---

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgresSQL
- Pytest
- Docker
