Project Planning System (Лабораторна 3)

Проєкт для автоматизації генерації, обробки та імпорту денормалізованих даних системи планування проєктів (проєкти, задачі, ресурси, призначення ресурсів) з CSV-файлу в реляційну базу даних. Додатково реалізовано повноцінний веб-інтерфейс на основі патерну MVC (Model-View-Controller) для виконання CRUD-операцій над основною сутністю — «Проєкт».

Проєкт побудований з використанням суворої трирівневої архітектури, шаблонів Інверсія управління (IoC) та Впровадження залежностей (DI).

Технології
- Мова: Python 3.10+
- Framework: Flask 3.0+ (веб-сервер та маршрутизація), Flask-RESTX (REST API та Swagger UI)
- Шаблонізатор (View): Jinja2 (генерація HTML-сторінок)
- UI/UX: Bootstrap 5 (стилізація форм, таблиць, прогрес-барів)
- ORM: SQLAlchemy 2.0+
- База даних: SQLite (вбудована, драйвер sqlite3)
- Формат даних: єдиний денормалізований .csv файл (1000+ рядків)

Архітектура проєкту (Layered Architecture + MVC)
Проєкт розділений на незалежні шари. Бізнес-логіка повністю ізольована від деталей реалізації бази даних та веб-фреймворку за допомогою інтерфейсів. Для веб-частини імплементовано класичний патерн MVC.

Структура шарів

1. DAL (Data Access Layer / Model) — Рівень доступу до даних (data_access/)

- interfaces/: абстрактні класи (IProjectRepository, ITaskRepository, IResourceRepository, ICsvReader), які визначають контракти. Розширено методами для CRUD-операцій.
- models/: ORM-моделі таблиць бази даних із налаштованими зв'язками (projects, tasks, resources, task_resources).
- repositories/: інкапсулює логіку запитів до бази даних через SQLAlchemy ORM (додавання, редагування, видалення та пошук сутностей).
- csv_reader.py: відповідає за читання сирих даних з файлової системи.

2. BLL (Business Logic Layer) — Рівень бізнес-логіки (business_logic/)

- interfaces/: контракти сервісів (IProjectService, ITaskService, IResourceService, IPlanService).
- services/: реалізація бізнес-правил:
  - project_service.py: CRUD проєктів, розрахунок прогресу, валідація плану.
  - task_service.py: CRUD задач, оновлення статусів, призначення ресурсів.
  - resource_service.py: CRUD людських та матеріальних ресурсів.
  - plan_service.py: імпорт з CSV, побудова об'єктів та збереження в БД.
- Залежить виключно від абстрактних інтерфейсів DAL.

3. Presentation Layer (Controllers & Views) — Презентаційний рівень (presentation/)

- api/ (REST API, Лаб 2): Flask-RESTX ендпоінти, Swagger UI, JSON-серіалізатори.
- web/ (MVC, Лаб 3):
  - controllers/ (Controller): Flask Blueprint-контролери. Приймають HTTP-запити, звертаються до Моделі через бізнес-сервіси та повертають HTML-сторінки.
    - project_controller.py: список, деталі, створення, редагування, видалення проєктів.
    - task_controller.py: CRUD задач, управління статусами та призначення ресурсів.
    - resource_controller.py: CRUD людських і матеріальних ресурсів.
  - templates/ (View): Jinja2 HTML-шаблони для візуалізації даних (таблиці, форми, прогрес-бари, статистика).
  - app.py: точка входу MVC-додатку, реєстрація Blueprint'ів.

Infrastructure (infrastructure/)

- config.py: конфігурація застосунку (DATABASE_URL, CSV_FILE_PATH, DEBUG).
- database.py: ініціалізація SQLAlchemy engine/session та створення таблиць.
- di_container.py: IoC/DI контейнер, який зв'язує BLL-сервіси через інтерфейси DAL.

Дані та утиліти
- data/data.csv: вхідний файл для імпорту (60 проєктів, 840 задач, 250 ресурсів, 1700+ призначень).
- data/project_planning.db: SQLite база даних (створюється автоматично).
- scripts/generate_csv.py: CLI-генератор CSV (1000+ рядків).

Інструкція із запуску

1. Встановлення залежностей
Переконайтеся, що ви знаходитесь у віртуальному середовищі проєкту. Встановіть всі необхідні бібліотеки з файлу requirements.txt:

pip install -r requirements.txt

2. Генерація тестових даних
Для первинного наповнення програми згенеруйте CSV-файл (понад 1000 рядків), який з'явиться у папці data/:

python3 scripts/generate_csv.py

3. Імпорт даних у базу даних (Лаб 2)
Запустіть REST API та імпортуйте CSV через Swagger або виконайте імпорт напряму:

python3 presentation/api/app.py
# відкрийте http://localhost:8000/swagger → POST /plan/import

4. Запуск веб-додатку MVC (Лаб 3)
Запустіть MVC Flask-додаток. SQLite БД створиться автоматично під час першого запуску:

python3 -c "import sys,os; sys.path.insert(0,os.getcwd()); \
  from presentation.web.app import app; \
  app.run(host='0.0.0.0', port=5001)"

5. Робота з веб-інтерфейсом MVC
Відкрийте браузер та перейдіть за адресою: http://localhost:5001

Через зручний UI ви можете:
- Переглядати список усіх проєктів з прогресом виконання.
- Відкривати деталі проєкту: задачі, статистика, валідація плану.
- Додавати нові проєкти, задачі та ресурси через HTML-форми.
- Редагувати існуючі записи (назва, дати, статус, тривалість тощо).
- Видаляти сутності з бази даних.
- Призначати та відкріплювати ресурси від задач.
- Оновлювати статус задач (pending → in_progress → completed → on_hold).

REST API (Лаб 2)
Swagger UI доступний за адресою: http://localhost:8000/swagger

Ключові ендпоінти:
- Projects: /projects/
- Tasks: /tasks/
- Resources: /resources/
- Plan import/export: /plan/
- Plan import: POST /plan/import
- Plan export: GET /plan/<project_id>/export
- Plan validation: GET /plan/<project_id>/validate

Примітки
- За замовчуванням використовується SQLite: data/project_planning.db.
- Шлях до CSV можна перевизначити змінною середовища CSV_FILE_PATH.
- Шлях до БД можна перевизначити змінною середовища DATABASE_URL.
