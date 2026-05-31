import json
from typing import Dict, Any, List
from datetime import datetime

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class KafkaOutputStrategy(IOutputStrategy):
    """
    Outputs messages to Apache Kafka.
    Suitable for streaming data to event brokers, log aggregation, or distributed systems.
    
    Configuration via environment variables:
      - KAFKA_BOOTSTRAP_SERVERS: comma-separated broker addresses (default: localhost:9092)
      - KAFKA_TOPIC: topic name (default: data-output)
    """

    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "data-output"):
        """Initialize Kafka producer."""
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        self._connect()

    def _connect(self) -> None:
        """Connect to Kafka broker."""
        try:
            from kafka import KafkaProducer
            
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            print(f"✅ Kafka підключено: {self.bootstrap_servers}")
        except ImportError:
            raise ImportError(
                "kafka-python не встановлено. Встановіть: pip install kafka-python"
            )
        except Exception as e:
            raise RuntimeError(f"Помилка підключення до Kafka: {e}")

    def output(self, message: str) -> None:
        """Send a single message to Kafka."""
        if not self.producer:
            return
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "type": "text",
        }
        try:
            self.producer.send(self.topic, value=payload)
        except Exception as e:
            print(f"❌ Помилка відправки в Kafka: {e}")

    def output_dict(self, data: Dict[str, Any]) -> None:
        """Send a dictionary as a Kafka message."""
        if not self.producer:
            return
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "statistics",
            "data": data,
        }
        try:
            self.producer.send(self.topic, value=payload)
            print(f"✅ Статистика відправлена в Kafka: {data}")
        except Exception as e:
            print(f"❌ Помилка відправки статистики в Kafka: {e}")

    def output_list(self, items: List[str]) -> None:
        """Send a list of items to Kafka."""
        if not self.producer:
            return
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "list",
            "items": items,
        }
        try:
            self.producer.send(self.topic, value=payload)
            print(f"✅ Список відправлений в Kafka ({len(items)} елементів)")
        except Exception as e:
            print(f"❌ Помилка відправки списку в Kafka: {e}")

    def flush(self) -> None:
        """Ensure all messages are sent."""
        if self.producer:
            try:
                self.producer.flush()
                print("✅ Kafka producer очищено (flush)")
            except Exception as e:
                print(f"❌ Помилка flush Kafka: {e}")
            finally:
                self.producer.close()
                self.producer = None
