# 🛠️ Техническое задание на разработку API для сервиса записи в частные клиники (FastAPI) 🏥

### 1. **📝 Общее описание**
API предназначено для взаимодействия мобильного приложения и веб-интерфейса с серверной частью сервиса записи в частные клиники. API должно поддерживать:
- Управление данными клиник, врачей, услуг и пользователей.
- Авторизацию и регистрацию пользователей с использованием JWT.
- Оплату через тестовую платежную систему Сбера.
- Чат между пользователями и врачами через WebSocket.
- Запись клиента на услугу к врачу в клинике.

---

### 2. **🚀 Функциональные требования**

#### 2.1 **👤 Пользователи**
- **Регистрация пользователя**:
  - Эндпоинт: `POST /api/v1/auth/register`
  - Поля: `email`, `password`, `full_name`, `phone`.
  - Ответ: `id`, `email`, `full_name`, `phone`.
- **Авторизация пользователя**:
  - Эндпоинт: `POST /api/v1/auth/login`
  - Поля: `email`, `password`.
  - Ответ: JWT-токен (access и refresh).
- **Обновление токена**:
  - Эндпоинт: `POST /api/v1/auth/refresh`
  - Поля: `refresh_token`.
  - Ответ: новый JWT-токен.
- **Получение профиля пользователя**:
  - Эндпоинт: `GET /api/v1/users/me`
  - Требуется авторизация.
  - Ответ: `id`, `email`, `full_name`, `phone`.

#### 2.2 **🏥 Клиники**
- **Получение списка клиник**:
  - Эндпоинт: `GET /api/v1/clinics`
  - Параметры: `limit`, `offset`, `search` (поиск по названию).
  - Ответ: список клиник с полями `id`, `name`, `address`, `logo_url`.
- **Получение деталей клиники**:
  - Эндпоинт: `GET /api/v1/clinics/{clinic_id}`
  - Ответ: `id`, `name`, `address`, `description`, `logo_url`, `rating`.
- **Добавление клиники в избранное**:
  - Эндпоинт: `POST /api/v1/clinics/{clinic_id}/favorite`
  - Требуется авторизация.
- **Удаление клиники из избранного**:
  - Эндпоинт: `DELETE /api/v1/clinics/{clinic_id}/favorite`
  - Требуется авторизация.

#### 2.3 **👨‍⚕️ Врачи**
- **Получение списка врачей**:
  - Эндпоинт: `GET /api/v1/doctors`
  - Параметры: `limit`, `offset`, `search` (поиск по имени), `clinic_id` (фильтр по клинике).
  - Ответ: список врачей с полями `id`, `full_name`, `specialization`, `photo_url`, `rating`.
- **Получение деталей врача**:
  - Эндпоинт: `GET /api/v1/doctors/{doctor_id}`
  - Ответ: `id`, `full_name`, `specialization`, `description`, `photo_url`, `rating`.
- **Добавление врача в избранное**:
  - Эндпоинт: `POST /api/v1/doctors/{doctor_id}/favorite`
  - Требуется авторизация.
- **Удаление врача из избранного**:
  - Эндпоинт: `DELETE /api/v1/doctors/{doctor_id}/favorite`
  - Требуется авторизация.

#### 2.4 **🩺 Услуги**
- **Получение списка услуг**:
  - Эндпоинт: `GET /api/v1/services`
  - Параметры: `limit`, `offset`, `search` (поиск по названию), `clinic_id` (фильтр по клинике), `doctor_id` (фильтр по врачу).
  - Ответ: список услуг с полями `id`, `name`, `description`, `price`, `duration`.
- **Получение деталей услуги**:
  - Эндпоинт: `GET /api/v1/services/{service_id}`
  - Ответ: `id`, `name`, `description`, `price`, `duration`, `clinic_id`, `doctor_id`.

#### 2.5 **📅 Записи на прием**
- **Создание записи на прием**:
  - Эндпоинт: `POST /api/v1/appointments`
  - Поля: `clinic_id`, `doctor_id`, `service_id`, `date`, `time`.
  - Требуется авторизация.
  - Ответ: `id`, `clinic_id`, `doctor_id`, `service_id`, `date`, `time`, `status`.
- **Получение списка записей пользователя**:
  - Эндпоинт: `GET /api/v1/appointments`
  - Требуется авторизация.
  - Ответ: список записей с полями `id`, `clinic_id`, `doctor_id`, `service_id`, `date`, `time`, `status`.
- **Отмена записи**:
  - Эндпоинт: `DELETE /api/v1/appointments/{appointment_id}`
  - Требуется авторизация.

#### 2.6 **💳 Оплата**
- **Инициализация оплаты**:
  - Эндпоинт: `POST /api/v1/payment/create`
  - Поля: `appointment_id`, `amount`.
  - Требуется авторизация.
  - Ответ: `payment_id`, `payment_url` (для редиректа на страницу оплаты Сбера).
- **Подтверждение оплаты**:
  - Эндпоинт: `POST /api/v1/payment/confirm`
  - Поля: `payment_id`, `status` (успех/неудача).
  - Ответ: `success`.

Для тестирования оплаты использовать [тестовую среду Сбера](https://developer.sberbank.ru/doc/v1/acquiring/webservice-requests1pay).

#### 2.7 **💬 Чат (WebSocket)**
- **Подключение к чату**:
  - Эндпоинт: `ws://{host}/api/v1/chat`
  - Параметры: `user_id`, `token` (JWT).
  - Возможности:
    - Отправка сообщений: `{"type": "message", "content": "текст сообщения", "recipient_id": "id_получателя"}`.
    - Получение сообщений в реальном времени.
    - Уведомления о новых сообщениях.

---

### 3. **⚙️ Нефункциональные требования**
- **🚀 Производительность**: Время ответа API не должно превышать 500 мс.
- **🔒 Безопасность**:
  - Использование HTTPS.
  - Валидация всех входящих данных.
  - Защита от SQL-инъекций и XSS.
- **📝 Логирование**: Все запросы и ошибки должны логироваться.

---

### 4. **🛠️ Технологии**
- **Backend**: FastAPI.
- **База данных**: PostgreSQL.
- **Аутентификация**: JWT.
- **Оплата**: Сбербанк API (тестовая среда).
- **WebSocket**: `websockets` библиотека для FastAPI.

### 5. **📚 Дополнительные требования**
- Документация API должна быть реализована с использованием Swagger/OpenAPI.

Вот отформатированный текст:

---

### 📦 **Запуск проекта в Docker**

🔹 **Шаг 1: Клонируем репозиторий**
```bash
git clone https://github.com/your-repo/HealthLink-CoolPeppers-Backend.git
cd HealthLink-CoolPeppers-Backend
```

🔹 **Шаг 2: Запускаем контейнеры**
```bash
docker-compose up --build
```
✅ Запустятся:
- PostgreSQL на `localhost:5432`
- FastAPI на `localhost:8080`
- Swagger UI на [http://localhost:8080/docs](http://localhost:8080/docs)

🔹 **Шаг 3: Остановка контейнеров**
```bash
docker-compose down
```

---
