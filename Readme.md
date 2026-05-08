# ✈️ WhenFlight API

REST API на FastAPI для получения информации о рейсах и прогнозирования вероятности задержек.

Проект использует внешний API AeroDataBox (RapidAPI) и Redis для кеширования запросов.

---

# 🚀 Возможности

* Поиск рейсов по номеру и дате
* Получение информации о вылете и прибытии
* Прогноз вероятности задержки рейса
* Кеширование ответов через Redis
* Асинхронная архитектура
* Валидация данных через Pydantic
* Документация Swagger/OpenAPI

---

# 🛠️ Стек технологий

* Python 3.12+
* FastAPI
* Uvicorn
* Redis
* HTTPX
* Pydantic v2
* Pytest
* Poetry

---

# 📦 Установка

## 1. Клонирование репозитория

```bash
git clone https://github.com/Mellson7781/when-flight-api.git
cd when-flight-api
```

---

## 2. Установка зависимостей

### Через Poetry

```bash
poetry install
```

### Или через pip

```bash
pip install -r requirements.txt
```

---

# ⚙️ Настройка `.env`

Создайте файл `.env` в корне проекта.

Пример:

```env
APP_NAME=WhenFlight API
DEBUG=True
DESCRIPTION=API for flight search and delay forecast
VERSION=1.0.0

HOST=127.0.0.1
PORT=8000

RapidAPI_Key=your_rapidapi_key
RapidAPI_Host=aerodatabox.p.rapidapi.com

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

# 🔑 Получение API ключа

Проект использует AeroDataBox через RapidAPI.

1. Зарегистрируйтесь на RapidAPI
2. Подпишитесь на AeroDataBox API
3. Получите API Key
4. Укажите его в `.env`

---

# ▶️ Запуск проекта

## Запуск Redis

### Docker

```bash
docker run -d -p 6379:6379 redis
```

---

## Запуск приложения

```bash
python main.py
```

или:

```bash
uvicorn main:app --reload
```

---

# 📚 Swagger документация

После запуска:

* Swagger UI:

```text
http://127.0.0.1:8000/docs
```

* ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 📡 API Endpoints

## Проверка API

```http
GET /ping
```

---

## Поиск рейса

```http
GET /api/flight/searech/number
```

### Query параметры

| Параметр  | Тип    | Описание    |
| --------- | ------ | ----------- |
| number    | string | Номер рейса |
| LocalDate | date   | Дата рейса  |

### Пример запроса

```http
GET /api/flight/searech/number?number=LH1234&LocalDate=2026-03-30
```

### Пример ответа

```json
{
  "number": "LH 1234",
  "status": "Expected",
  "aircraft": "Airbus A320",
  "departure_iata": "FRA",
  "arrival_iata": "LHR",
  "airline": "Lufthansa"
}
```

---

## Прогноз задержки рейса

```http
GET /api/flight/forecast
```

### Пример запроса

```http
GET /api/flight/forecast?number=LH1234&LocalDate=2026-03-30
```

### Пример ответа

```json
{
  "chance_of_delay": "medium",
  "departure_airoport": {
    "airportIcao": "EDDF"
  },
  "arrival_airoport": {
    "airportIcao": "EGLL"
  }
}
```

---

# 🧠 Как работает прогноз

API получает:

* информацию о рейсе;
* статистику задержек аэропортов;
* вычисляет средний индекс задержек;
* определяет вероятность задержки:

| Delay Index | Статус |
| ----------- | ------ |
| < 1.0       | LOW    |
| < 3.0       | MEDIUM |
| >= 3.0      | HIGH   |

---

# 🗂️ Структура проекта

```text
app/
├── api/
│   └── routers/
├── common/
├── core/
├── dependencies/
├── error/
├── infrastructure/
├── schemas/
├── service/
│
main.py
pyproject.toml
```

---

# 🧪 Тестирование

```bash
pytest
```

---

# ⚡ Особенности проекта

* Асинхронная работа через `async/await`
* Redis кеширует запросы к внешнему API
* FastAPI dependency injection
* Разделение на service / infrastructure / schemas
* Typed architecture

---

# ❗ Известные особенности

В проекте присутствуют некоторые опечатки в route naming:

* `filght` вместо `flight`
* `searech` вместо `search`
* `forescast` вместо `forecast`

Они сохранены для совместимости с текущим API.

---

# 👨‍💻 Автор

GitHub: [https://github.com/Mellson7781](https://github.com/Mellson7781)
