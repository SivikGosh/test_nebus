#### СТРУКТУРА ПРОЕКТА СООТВЕТСТВУЕТ 'BEST PRACTICES': https://github.com/zhanymkanov/fastapi-best-practices .

# test4nebus
Тестовое задание для компании ~~Небус~~ Secunda.
Демо проекта доступно по адресу: http://nebus.eventfun.ru/.

### Стек технологий
<img src="https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/pydantic-%23E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/postgresql-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/docker-%232496ED.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/poetry-%2360A5FA.svg?style=for-the-badge&logo=poetry&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white" alt="Badge" />
<img src="https://img.shields.io/badge/gunicorn-%23499848.svg?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Badge" />

## Установка

### Клонировать репозиторий
```bash
$ git clone git@github.com:SivikGosh/test4nebus.git
```

### Перейти в директорию compose-файла и подготовить файлы конфигурации
```bash
$ cd nebus_compose/
$ cp .env.example .env
```

### Файлы концигурации
```bash
# .env

DB_HOST=db                  # контейнер БД
DB_PORT=5432                # порт контейнера
DB_NAME=postgres            # имя базы данных
DB_USER=postgres            # имя пользователя базы данных (он же POSTGRES_USER)
DB_PASS=postgres            # пароль пользователя базы данных (он же POSTGRES_PASSWORD)

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

SECRET=1qazxsw2             # статический API ключ

```

```bash
# nginx.conf

server {
    listen 80;
    server_name localhost;  # localhost заменить на домен или ip целевого сайта

    location / {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# docker-compose.yml

services:
  
  db:
    image: postgis/postgis
    volumes:
      - db_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    expose:
      - 5432

  backend:
    build:
      context: ../app/
    env_file:
      - ./.env
    expose:
      - 8000
    volumes:
      - logs:/app/logs/
    depends_on:
      - db
    restart: always

  nginx:
    image: nginx:1.19.3
    ports:
      - 80:80
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend

volumes:
  db_data:

```
<br>

<div align="right">

## Author's contact
<a href='https://t.me/sivikgosh' target='_blank'><img src='https://img.shields.io/badge/SivikGosh-white?style=flat-square&logo=Telegram&logoColor=26A5E4'></a>

</div>
