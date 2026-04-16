Project Planning System (Лабораторна 2)

Проєкт для автоматизації генерації, обробки та імпорту денормалізованих даних планування проєктів (проєкти, задачі, ресурси, призначення ресурсів) з одного CSV-файлу у реляційну базу даних. Проєкт побудований з використанням суворої трирівневої архітектури, шаблонів Інверсія управління (IoC) та Впровадження залежностей (DI).

Технології
- Мова: Python 3.10+
- Framework: Flask + Flask-RESTX (REST API та Swagger UI)
- ORM: SQLAlchemy 2.0+
- База даних: SQLite (вбудована, драйвер sqlite3)
- Формат даних: єдиний денормалізований CSV-файл (1000+ рядків)

Архітектура проєкту
Проєкт реалізований за принципом Layered Architecture (багатошарова архітектура). Бізнес-логіка ізольована від деталей реалізації БД через інтерфейси (абстрактні класи) та DI-контейнер.

Структура шарів
1. DAL (Data Access Layer) - рівень доступу до даних
Папка: data_access/

- interfaces/: контракти репозиторіїв та CSV-reader.
- models/: ORM-моделі таблиць (projects, tasks, resources, task_resources).
- repositories/: реалізації доступу до даних через SQLAlchemy.
- csv_reader.py: зчитування даних з CSV-файлу.

2. BLL (Business Logic Layer) - рівень бізнес-логіки
Папка: business_logic/

- interfaces/: контракти сервісів.
- services/: реалізація бізнес-правил:
  - project_service.py: CRUD проєктів, прогрес, валідація плану.
  - task_service.py: CRUD задач, статуси, призначення ресурсів.
  - resource_service.py: CRUD ресурсів.
  - plan_service.py: імпорт з CSV, побудова моделей та збереження в БД.

3. Presentation Layer - презентаційний рівень
Папка: presentation/

- interfaces/: інтерфейси контролерів (без бізнес-логіки).
- api/: Flask API-шар:
  - app.py: точка входу та ініціалізація API.
  - routes/: роутинг, згрупований по модулях (projects, tasks, resources, plan).
  - serializers.py: формування JSON-відповідей.
  - dependencies.py: доступ до DI-контейнера.

Infrastructure
Папка: infrastructure/

- config.py: конфігурація застосунку (DATABASE_URL, CSV_FILE_PATH, DEBUG).
- database.py: ініціалізація SQLAlchemy engine/session та створення таблиць.
- di_container.py: IoC/DI контейнер, який зв'язує BLL через інтерфейси DAL.

Дані та утиліти
- data/data.csv: вхідний файл для імпорту.
- data/project_planning.db: SQLite база даних (створюється автоматично).
- scripts/generate_csv.py: CLI-генератор CSV (1000+ рядків).

Інструкція із запуску
1. Встановлення залежностей
Переконайтеся, що ви у віртуальному середовищі проєкту, потім встановіть бібліотеки:

pip install -r requirements.txt

2. Генерація тестових даних
Згенеруйте один CSV-файл (за замовчуванням data/data.csv):

python3 scripts/generate_csv.py

3. Запуск сервера
Запустіть API. SQLite БД створиться автоматично під час першого запуску:

python3 presentation/api/app.py

4. Swagger та тестування ендпоінтів
Swagger UI доступний за адресою:

http://localhost:8000/swagger

Ключові ендпоінти
- Projects: /projects/
- Tasks: /tasks/
- Resources: /resources/
- Plan import: POST /plan/import
- Plan export: GET /plan/<project_id>/export
- Plan validation: GET /plan/<project_id>/validate

Примітки
- За замовчуванням використовується SQLite: data/project_planning.db.
- Шлях до CSV можна перевизначити змінною середовища CSV_FILE_PATH.
- Шлях до БД можна перевизначити змінною середовища DATABASE_URL.
