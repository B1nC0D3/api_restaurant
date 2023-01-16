# API для выдачи меню ресторана
Содержит в себе роуты на меню, подменю и блюда. В каждом меню может быть подменю, так же в кажом подменю может быть блюдо.
Подменю может принадлежать только к одному меню, а блюдо только к одному подменю.

---
## Запуск приложения
В корневой папке скачанного репозитория выполните:
```
    python3 -m venv venv # use 'python' instead 'python3' for Win
    source venv/bin/activate # source venv/Scripts/activate for Win
    pip3 install -r requirements.txt
    uvicorn main:app
```
 API будет доступен по адресу `127.0.0.1`. Документация доступна по `127.0.0.1/docs`.

 ---

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgresSQL 
