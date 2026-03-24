# TaskFlow — менеджер задач

Веб-приложение для управления личными задачами, разработанное на Django в рамках производственной практики. Проект основан на open‑source решении [Build a Todo List with Django and Test-Driven Development](http://www.obeythetestinggoat.com/) и адаптирован под собственную предметную область.


##  Возможности

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление задач
- Изменение статуса задачи (в работе / выполнено)
- Установка срока выполнения (deadline)
- Поиск задач
- Фильтрация по статусу, приоритету и категории
- Сортировка задач
- Управление категориями (добавление, редактирование, удаление)
- Административная панель Django для управления данными

---

##  Технологии

- **Backend**: Python 3.13, Django 5.2
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **База данных**: SQLite (локально), PostgreSQL (деплой)
- **Инструменты**: Git, GitHub, Code Climate, Render

---

##  Архитектура

Приложение построено по шаблону **MVT** (Model‑View‑Template) фреймворка Django:
Browser (Client)
│
▼
Django Templates (View)
│
▼
Django Views (Controller logic)
│
▼
Django Models (ORM)
│
▼
SQLite Database

text

- **Model** – описание структуры данных и бизнес‑логики.
- **View** – обработка HTTP‑запросов, взаимодействие с моделями.
- **Template** – отображение пользовательского интерфейса.

---

##  Модель данных (ERD)

Основные сущности и связи:

### User
| Поле       | Тип      |
|------------|----------|
| id         | integer  |
| username   | string   |
| password   | string   |
| email      | string   |
| role       | ForeignKey → Role |

### Role
| Поле | Тип     |
|------|---------|
| id   | integer |
| name | string  |

### Task
| Поле         | Тип          |
|--------------|--------------|
| id           | integer      |
| title        | string       |
| description  | text         |
| status       | string       |
| priority     | string       |
| due_date     | datetime     |
| created_at   | datetime     |
| updated_at   | datetime     |
| user         | ForeignKey → User |
| category     | ForeignKey → TaskCategory |

### TaskCategory
| Поле        | Тип     |
|-------------|---------|
| id          | integer |
| name        | string  |
| description | text    |

**Связи**:
- `Role 1 ─── N User`
- `User 1 ─── N Task`
- `TaskCategory 1 ─── N Task`

---

##  Основные сценарии использования (Use Case)

1. **Регистрация** – новый пользователь создаёт учётную запись.
2. **Авторизация** – вход в систему под своим логином и паролем.
3. **Создание задачи** – заполнение формы с названием, описанием, приоритетом, категорией и сроком.
4. **Редактирование задачи** – изменение любых полей существующей задачи.
5. **Изменение статуса** – перевод задачи в состояние «выполнена».
6. **Поиск и фильтрация** – быстрый поиск по названию, фильтр по статусу, приоритету, категории.
7. **Администрирование** – управление категориями через админ‑панель.

---

##  Деплой

Проект доступен по адресу:  
 [https://taskflow-nev3.onrender.com](https://taskflow-nev3.onrender.com)

Тестовые данные для входа:  
- **Логин:** `Admin`  
- **Пароль:** `admin`

---

## Локальный запуск

**Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Vitalij078/taskflow-django.git
   cd taskflow-django
 ```
**Создайте и активируйте виртуальное окружение:**
 ```bash
    python -m venv venv
    source venv/bin/activate        # Linux/Mac
    venv\Scripts\activate           # Windows
 ```
**Установите зависимости:**
 ```bash
    pip install -r requirements.txt
 ```
**Выполните миграции:**
 ```bash
    python manage.py migrate
 ```
**Создайте суперпользователя:**
 ```bash
    python manage.py createsuperuser
 ```
**Запустите сервер:**
 ```bash
    python manage.py runserver
 ```
**Откройте в браузере: http://127.0.0.1:8000**

## Демонстрация
[![FastPic.Org](https://i127.fastpic.org/thumb/2026/0325/f4/_30c9b24e5a31266cb5d65dbec7e998f4.jpeg)](https://fastpic.org/view/127/2026/0325/_30c9b24e5a31266cb5d65dbec7e998f4.gif.html)