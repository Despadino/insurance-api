# 📖 Инструкция по запуску проекта  

## Содержание
1. [Общее описание](#общее-описание)  
2. [Требования](#требования)  
3. [Клонирование репозитория](#клонирование-репозитория)  
4. [Установка зависимостей](#установка-зависимостей)  
5. [Настройка окружения (`.env`)](#настройка-окружения-env)  
6. [Генерация сертификатов](#генерация-сертификатов)  
7. [Запуск в режиме разработки](#запуск-в-режиме-разработки)  
8. [Запуск в Docker Compose (production‑like)](#запуск-в-docker-compose)  
9. [Работа с базой данных](#работа-с-базой-данных)  
10. [Полезные команды Makefile](#полезные-команды-makefile)  
11. [FAQ / распространённые ошибки](#faq)  

---

## Общее описание  

Проект – это микросервис **insurance‑api**, написанный на **FastAPI** и использующий:

| Сервис | Технология | Где запускается |
|--------|------------|-----------------|
| API‑сервер | FastAPI (Python) | Локально (через `poetry run python -m main`) |
| База данных | PostgreSQL | Docker Compose |
| Кеш | Redis | Docker Compose |
| LLM‑модель | Ollama | **Локальная** установка, не в Docker |
| Миграции | Alembic | Запускаются из контейнера или локально |

Все сервисы, кроме **Ollama**, работают в Docker‑композиции.  

---

## Требования  

| Требование | Версия / Примечание |
|------------|---------------------|
| Python | 3.10+ (рекомендовано 3.11) |
| Poetry | 1.7+ |
| Docker & Docker‑Compose | 24.0+ |
| OpenSSL (для сертификатов) | любой |
| Ollama | локальная установка, см. https://github.com/ollama/ollama |
| Git | любой |

> **Важно:** Ollama **не** входит в Docker‑Compose – её нужно установить и запустить на хост‑машине вручную.

---

## Клонирование репозитория  

```bash
git clone https://github.com/your-org/insurance-api.git
cd insurance-api
```

---

## Установка зависимостей  

```bash
# Установить Poetry, если ещё нет
curl -sSL https://install.python-poetry.org | python3 -

# Установить зависимости проекта (без установки самого пакета)
make install
```

> В `Makefile` команда `install` эквивалентна  
> `poetry install --no-root`

---

## Настройка окружения (`.env`)  

1. Скопируйте шаблон:

   ```bash
   cp .env.example .env
   ```

2. Откройте `.env` в любимом редакторе и заполните переменные:

   ```dotenv
   # -----------------------
   # Общие параметры
   # -----------------------
   PROJECT_TITLE=Insurance API
   FAST_API_PORT=8000

   # -----------------------
   # PostgreSQL
   # -----------------------
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=insurance

   # -----------------------
   # Redis
   # -----------------------
   REDIS_PORT=6379
   REDIS_PASSWORD=redispwd

   # -----------------------
   # Ollama (локальная)
   # -----------------------
   OLLAMA_HOST=http://127.0.0.1:11434
   OLLAMA_MODEL=llama2:13b
   ```

### Что где используется  

| Переменная | Где используется |
|------------|-------------------|
| `FAST_API_PORT` | Порт, на котором слушает FastAPI (по умолчанию 8000) |
| `POSTGRES_*` | Параметры подключения к PostgreSQL (контейнер `db`) |
| `REDIS_*` | Параметры подключения к Redis (контейнер `redis`) |
| `OLLAMA_HOST` / `OLLAMA_MODEL` | URL и название модели Ollama, запущенной локально |

> **Важно:** Ollama должна быть доступна по указанному `OLLAMA_HOST`. Если вы меняете порт или IP, обновите переменные в `.env`.

---

## Генерация сертификатов  

Для взаимодействия с внешними системами (или при работе через HTTPS) требуется набор сертификатов, находящихся в  

```
insurance-api/app/core/certs/
```

Внутри каталога уже есть **README** с инструкциями, но основные шаги повторим здесь.

### Шаги

```bash
# Перейти в каталог сертификатов
cd insurance-api/app/core/certs

# 1. Создать закрытый ключ
openssl genrsa -out private.key 4096

# 2. Сгенерировать запрос на сертификат (CSR)
openssl req -new -key private.key -out request.csr \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=Insurance Ltd/OU=IT/CN=insurance-api.local"

# 3. Самоподписать сертификат (valid 365 дней)
openssl x509 -req -days 365 -in request.csr -signkey private.key -out certificate.crt

# 4. (Опционально) собрать цепочку в один файл
cat certificate.crt private.key > server.pem
```

### Что дальше  

- `private.key` – закрытый ключ (необходимо хранить в секрете).  
- `certificate.crt` – публичный сертификат.  
- `server.pem` – удобный файл, если ваш сервер принимает сертификат+ключ в одном файле.  

**Не забывайте добавить пути к сертификатам в переменные окружения, если ваш код их требует.**  

---

## Запуск в режиме разработки  

### 1. Убедиться, что Ollama запущена  

```bash
ollama serve     # запустит сервер Ollama на 127.0.0.1:11434
ollama pull $OLLAMA_MODEL   # загрузить нужную модель, например: llama2:13b
```

### 2. Запустить FastAPI без Docker  

```bash
make dev
```

Команда `make dev` выполнит:

```bash
poetry run python -m main
```

API будет доступен по адресу `http://127.0.0.1:<FAST_API_PORT>` (по умолчанию `8000`).  

---

## Запуск в Docker Compose  

Все сервисы (PostgreSQL, Redis, сам API) будут подняты в контейнерах, а Ollama — на хосте.  

```bash
make deploy
```

Это эквивалентно:

```bash
docker compose -f docker/docker-compose.yml --project-directory . up --build
```

### Что происходит  

| Сервис | Образ | Порт (на хосте) |
|--------|-------|-----------------|
| **api** | `insurance-api:latest` (собран из `Dockerfile`) | `<FAST_API_PORT>` (пример: 8000) |
| **db** | `postgres:15` | `5432` (по `POSTGRES_PORT`) |
| **redis** | `redis:7-alpine` | `6379` (по `REDIS_PORT`) |

#### Остановить и удалить всё

```bash
docker compose -f docker/docker-compose.yml down -v
```

---

## Работа с базой данных  

### Миграции  

Проект использует **Alembic**.  

| Команда | Описание |
|---------|----------|
| `make migration` | Создать новую миграцию с автогенерацией (`alembic revision --autogenerate -m "auto"`) |
| `make head` | Применить все миграции до последней версии (`alembic upgrade head`) |
| `make revision` | Запустить `alembic revision` вручную (можно добавить `-m "msg"`). |

### Загрузка актуальной БД  

Если у вас есть дамп (например, от продакшна) – выполните:

```bash
# 1. Скопировать дамп в каталог проекта
cp /path/to/dump.sql ./docker/initdb/dump.sql

# 2. Перезапустить контейнер БД (если уже работает)
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d db

# 3. Восстановить дамп
docker exec -i insurance-api-db-1 psql -U $POSTGRES_USER -d $POSTGRES_DB < ./docker/initdb/dump.sql
```

> **Заметка:** имя контейнера `insurance-api-db-1` может отличаться – проверьте вывод `docker ps`.

После восстановления можете выполнить `make head`, чтобы убедиться, что все миграции применены к актуальному состоянию схемы.

---

## Полезные команды Makefile  

| Цель | Что делает |
|------|------------|
| `make dev` | Запускает API локально через Poetry. |
| `make deploy` | Поднимает Docker‑Compose со сборкой образов. |
| `make migration` | Создаёт автоматическую миграцию Alembic. |
| `make revision` | Запускает `alembic revision --autogenerate`. |
| `make head` | Применяет миграции до последней версии. |
| `make install` | Устанавливает зависимости проекта (без установки самого пакета). |

---

## FAQ  

**1. Ollama не отвечает / получает `ConnectionRefusedError`**  
- Убедитесь, что сервис запущен: `ollama serve`.  
- Проверьте переменную `OLLAMA_HOST` в `.env`. По умолчанию `http://127.0.0.1:11434`.  
- Если используете Docker Desktop с WSL2, убедитесь, что контейнеры могут обратиться к хост‑машине (`host.docker.internal`), но в нашем случае Ollama работает **вне Docker**, так что проблем не должно быть.

**2. Ошибка при `make install`: Poetry не найден**  
- Установите Poetry глобально (`curl -sSL https://install.python-poetry.org | python3 -`).  
- Добавьте `$HOME/.local/bin` в `PATH` (обычно делается в `~/.bashrc` или `~/.zshrc`).

**3. База данных не стартует в Docker compose**  
- Проверьте, не заняты ли порты `5432` и `6379`.  
- Очистите тома: `docker compose down -v`.  

**4. Необходимо добавить новые переменные в `.env`**  
- Добавьте их в файл и перезапустите соответствующий сервис (Docker compose или локальный).  

**5. Как изменить порт FastAPI, не меняя код?**  
- Отредактируйте `FAST_API_PORT` в `.env`. При запуске через Docker compose (цель `deploy`) переменная будет передана в контейнер через `environment:` в `docker-compose.yml`.  

---

## Заключение  

Теперь у вас есть полностью рабочее окружение:

- **Локальная** разработка через `make dev` (FastAPI + Ollama).  
- **Контейнеризованное** окружение через `make deploy` (PostgreSQL, Redis, API).  
- Автоматическое управление схемой БД через Alembic.  
- Самостоятельно сгенерированные сертификаты для HTTPS/защищённого взаимодействия.  

Если возникнут вопросы, откройте *Issue* в репозитории или обратитесь к старшему разработчику проекта.  

**Удачной разработки!** 🚀  