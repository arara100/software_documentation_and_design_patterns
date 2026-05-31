# ЛР4: Реалізація GoF-паттерну Strategy

## 📌 Огляд задачі

**Мета:** Відділити код виводу рядків в консоль від коду читання даних з файлу, використовуючи паттерн **Strategy** (Стратегія).

**Результат:** Дозволити переключення виводу з консолі на Kafka, файл та інші цілі з **мінімальними змінами в коді** (лише через конфіграцію).

---

## 🎯 Реалізація паттерну Strategy

### 1. **Інтерфейс Strategy** (`IOutputStrategy`)

```python
# business_logic/interfaces/i_output_strategy.py

class IOutputStrategy(ABC):
    @abstractmethod
    def output(self, message: str) -> None:
        """Output a single message."""
        pass

    @abstractmethod
    def output_dict(self, data: Dict[str, Any]) -> None:
        """Output a dictionary (e.g., import statistics)."""
        pass

    @abstractmethod
    def output_list(self, items: List[str]) -> None:
        """Output a list of items."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Ensure all data is sent/written (cleanup/finalize)."""
        pass
```

### 2. **Конкретні реалізації (Strategies)**

#### a) **ConsoleOutputStrategy** — вивід в консоль

```python
# business_logic/strategies/console_output_strategy.py

class ConsoleOutputStrategy(IOutputStrategy):
    def output(self, message: str) -> None:
        print(message)

    def output_dict(self, data: Dict[str, Any]) -> None:
        print("\n" + "=" * 60)
        print("📊 Статистика імпорту:")
        for key, value in data.items():
            print(f"  {key.capitalize()}: {value}")
        print("=" * 60 + "\n")

    def output_list(self, items: List[str]) -> None:
        print("\n📋 Список елементів:")
        for idx, item in enumerate(items, 1):
            print(f"  {idx}. {item}")
        print()

    def flush(self) -> None:
        pass  # No cleanup needed for console
```

#### b) **KafkaOutputStrategy** — вивід в Apache Kafka

```python
# business_logic/strategies/kafka_output_strategy.py

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "data-output"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(...)

    def output(self, message: str) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "type": "text",
        }
        self.producer.send(self.topic, value=payload)

    # ... інші методи ...

    def flush(self) -> None:
        self.producer.flush()
        self.producer.close()
```

#### c) **FileOutputStrategy** — вивід в файл (JSONL)

```python
# business_logic/strategies/file_output_strategy.py

class FileOutputStrategy(IOutputStrategy):
    def __init__(self, file_path: str = "output/log.jsonl"):
        self.file_path = file_path

    def output(self, message: str) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "type": "text",
        }
        self._write_line(payload)

    def _write_line(self, data: Dict[str, Any]) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    # ... інші методи ...
```

---

## 🔧 Інтеграція в бізнес-логіку

### **PlanService** використовує OutputStrategy

```python
# business_logic/services/plan_service.py

class PlanService(IPlanService):
    def __init__(
        self,
        project_repo: IProjectRepository,
        task_repo: ITaskRepository,
        resource_repo: IResourceRepository,
        csv_reader: ICsvReader,
        output_strategy: IOutputStrategy,  # ← Strategy інжектується
    ) -> None:
        self._output_strategy = output_strategy

    def import_from_csv(self, file_path: str) -> Dict:
        # Читання даних
        rows = self._csv_reader.read(file_path)
        self._output_strategy.output(f"📂 Читання CSV файлу: {file_path}")

        # ... обробка даних ...

        # Вивід результатів через стратегію
        stats = {
            "projects": len(projects),
            "tasks": len(tasks),
            "resources": len(resources),
            "assignments": len(assignments),
        }
        self._output_strategy.output_dict(stats)
        self._output_strategy.flush()

        return stats
```

---

## ⚙️ Конфіграція

### **Config** з параметрами Strategy

```python
# infrastructure/config.py

class Config:
    # ================================================================
    # Output Strategy Configuration (ЛР4)
    # ================================================================
    OUTPUT_STRATEGY: str = os.getenv("OUTPUT_STRATEGY", "console").lower()
    # Дозволені: "console", "kafka", "file"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "data-output")

    # File
    OUTPUT_FILE_PATH: str = os.getenv(
        "OUTPUT_FILE_PATH",
        os.path.join(PROJECT_ROOT, "output", "log.jsonl"),
    )
```

### **DIContainer** — Factory для створення Strategy

```python
# infrastructure/di_container.py

class DIContainer:
    def __init__(self):
        self._output_strategy = self._create_output_strategy()

    def _create_output_strategy(self) -> IOutputStrategy:
        """Factory method: вибір стратегії на основі конфіку."""
        strategy_type = Config.OUTPUT_STRATEGY.lower()

        if strategy_type == "kafka":
            return KafkaOutputStrategy(
                bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                topic=Config.KAFKA_TOPIC,
            )
        elif strategy_type == "file":
            return FileOutputStrategy(file_path=Config.OUTPUT_FILE_PATH)
        else:  # default: console
            return ConsoleOutputStrategy()

    def get_plan_service(self) -> PlanService:
        return PlanService(
            self._project_repo,
            self._task_repo,
            self._resource_repo,
            self._csv_reader,
            self._output_strategy,  # ← Інжекція стратегії
        )
```

---

## 🚀 Використання

### **Вивід в консоль (за замовчуванням)**
```bash
python scripts/test_output_strategy.py
# або явно:
OUTPUT_STRATEGY=console python scripts/test_output_strategy.py
```

**Результат:**
```
==============================================================
📊 Статистика імпорту:
==============================================================
  Projects: 10
  Tasks: 85
  Resources: 42
  Assignments: 120
==============================================================
```

### **Вивід в файл**
```bash
OUTPUT_STRATEGY=file python scripts/test_output_strategy.py
```

**Результат:** Дані записані в `output/log.jsonl` у форматі JSONL:
```json
{"timestamp": "2026-05-12T10:30:45.123456", "type": "statistics", "data": {"projects": 10, ...}}
```

### **Вивід в Kafka**
```bash
OUTPUT_STRATEGY=kafka KAFKA_BOOTSTRAP_SERVERS=localhost:9092 python scripts/test_output_strategy.py
```

**Результат:** Дані відправлені в Kafka топік `data-output`

### **Кастомні параметри**
```bash
# Файл у кастомному місці
OUTPUT_FILE_PATH=reports/import_log.jsonl OUTPUT_STRATEGY=file python scripts/test_output_strategy.py

# Kafka з кастомним топіком
KAFKA_TOPIC=project-imports OUTPUT_STRATEGY=kafka python scripts/test_output_strategy.py
```

---

## 📊 Архітектура

```
┌─────────────────────────────────────────────────────────────┐
│                    PlanService                              │
│  (використовує OutputStrategy для виводу)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ залежить від
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              <<interface>>                                   │
│            IOutputStrategy                                   │
│  + output(message: str)                                      │
│  + output_dict(data: Dict)                                   │
│  + output_list(items: List)                                  │
│  + flush()                                                   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
    Реалізує           Реалізує             Реалізує
         │                    │                    │
    ┌────▼────────┐  ┌────────▼──────┐  ┌─────────▼─────┐
    │   Console   │  │    Kafka      │  │     File      │
    │  Strategy   │  │   Strategy    │  │   Strategy    │
    └─────────────┘  └───────────────┘  └───────────────┘
         │                    │                    │
    Консоль (stdout)    Apache Kafka      JSONL файл
```

---

## ✅ Переваги паттерну Strategy

1. **Відділення логіки:**
   - Логіка читання даних (CSV) **відділена** від логіки виводу
   - Кожна стратегія виходу має **одну відповідальність**

2. **Легко розширюється:**
   - Додати нову стратегію (HTTP, Email, S3) — додати новий клас, що реалізує `IOutputStrategy`
   - Ніяких змін в `PlanService`

3. **Конфігурація без коду:**
   - Переключення стратегій через **ENV змінні**
   - Не потрібно перекомпілювати/перезапускати з новим кодом

4. **Тестування:**
   - Можна легко mock `IOutputStrategy` для unit тестів
   - Без реальних залежностей (Kafka, файл)

5. **Runtime гнучкість:**
   - Вибір стратегії на основі конфіки під час запуску
   - Один docker image → різні конфіги → різні поведінки

---

## 🧪 Тестування

### **Unit тест з mock стратегією**

```python
from unittest.mock import Mock
from business_logic.services.plan_service import PlanService

def test_import_uses_output_strategy():
    # Arrange
    mock_strategy = Mock(spec=IOutputStrategy)
    service = PlanService(
        mock_project_repo, mock_task_repo, mock_resource_repo,
        mock_csv_reader, mock_strategy
    )

    # Act
    service.import_from_csv("test.csv")

    # Assert
    mock_strategy.output_dict.assert_called_once()
    mock_strategy.flush.assert_called_once()
```

---

## 📝 Файлова структура

```
business_logic/
├── interfaces/
│   └── i_output_strategy.py       # ← Інтерфейс Strategy
├── strategies/                     # ← Папка стратегій (ЛР4)
│   ├── __init__.py
│   ├── console_output_strategy.py  # Консоль
│   ├── kafka_output_strategy.py    # Kafka
│   └── file_output_strategy.py     # Файл
└── services/
    └── plan_service.py             # Використовує OutputStrategy

infrastructure/
├── config.py                       # Конфіг зі змінними Strategy
└── di_container.py                 # Factory для створення Strategy

scripts/
└── test_output_strategy.py         # CLI тест паттерну Strategy
```

---

## 🔗 Зв'язок з ЛР №7

Цей паттерн дозволяє логувати/аудирувати всі операції над БД в зручному форматі без змін в коді БД операцій. Наприклад:
- Записувати журнал змін в Kafka для real-time моніторингу
- Експортувати дані в S3 для backup
- Відправляти оповіщення по імейлу при важливих подіях

---

**Реалізовано:** ✅ ЛР4 — Паттерн Strategy для виводу даних
