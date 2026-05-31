import json
from typing import Dict, Any, List
from datetime import datetime

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class RedisOutputStrategy(IOutputStrategy):
    """
    Outputs messages to Redis.
    
    Supports two modes (via REDIS_MODE env variable):
      - "pubsub" (default): publishes messages to a Redis channel (real-time streaming)
      - "list": appends messages to a Redis list (persistent queue / log)
    
    Configuration via environment variables:
      - REDIS_HOST: Redis host (default: localhost)
      - REDIS_PORT: Redis port (default: 6379)
      - REDIS_PASSWORD: Redis password (default: None)
      - REDIS_DB: Redis database index (default: 0)
      - REDIS_CHANNEL: channel/key name (default: data-output)
      - REDIS_MODE: "pubsub" or "list" (default: pubsub)
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str = None,
        db: int = 0,
        channel: str = "data-output",
        mode: str = "pubsub",
    ):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.channel = channel
        self.mode = mode
        self.client = None
        self._connect()

    def _connect(self) -> None:
        try:
            import redis

            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True,
            )
            self.client.ping()
            print(f"✅ Redis підключено: {self.host}:{self.port} (режим: {self.mode})")
        except ImportError:
            raise ImportError(
                "redis не встановлено. Встановіть: pip install redis"
            )
        except Exception as e:
            raise RuntimeError(f"Помилка підключення до Redis: {e}")

    def _send(self, payload: Dict[str, Any]) -> None:
        if not self.client:
            return
        data = json.dumps(payload, ensure_ascii=False)
        try:
            if self.mode == "list":
                self.client.rpush(self.channel, data)
            else:
                self.client.publish(self.channel, data)
        except Exception as e:
            print(f"❌ Помилка відправки в Redis: {e}")

    def output(self, message: str) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "text",
            "message": message,
        }
        self._send(payload)

    def output_dict(self, data: Dict[str, Any]) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "statistics",
            "data": data,
        }
        self._send(payload)
        print(f"✅ Статистика відправлена в Redis [{self.mode}:{self.channel}]: {data}")

    def output_list(self, items: List[str]) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "list",
            "items": items,
        }
        self._send(payload)
        print(f"✅ Список відправлений в Redis ({len(items)} елементів)")

    def flush(self) -> None:
        if self.client:
            try:
                self.client.close()
                print("✅ Redis з'єднання закрито")
            except Exception as e:
                print(f"❌ Помилка закриття Redis: {e}")
            finally:
                self.client = None
