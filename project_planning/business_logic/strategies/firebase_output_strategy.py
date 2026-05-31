from typing import Dict, Any, List
from datetime import datetime

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class FirebaseOutputStrategy(IOutputStrategy):
    """
    Outputs messages to Firebase Realtime Database.
    
    Each call appends a new timestamped document under the configured path.
    
    Configuration via environment variables:
      - FIREBASE_CREDENTIALS_PATH: path to service account JSON key file
      - FIREBASE_DATABASE_URL: Firebase Realtime Database URL
                               e.g. https://<project-id>.firebaseio.com
      - FIREBASE_DB_PATH: root path in the database (default: output-logs)
    """

    def __init__(
        self,
        credentials_path: str,
        database_url: str,
        db_path: str = "output-logs",
    ):
        self.credentials_path = credentials_path
        self.database_url = database_url
        self.db_path = db_path
        self.db = None
        self._connect()

    def _connect(self) -> None:
        try:
            import firebase_admin
            from firebase_admin import credentials, db

            if not firebase_admin._apps:
                cred = credentials.Certificate(self.credentials_path)
                firebase_admin.initialize_app(cred, {"databaseURL": self.database_url})

            self.db = db
            print(f"✅ Firebase підключено: {self.database_url} (шлях: {self.db_path})")
        except ImportError:
            raise ImportError(
                "firebase-admin не встановлено. Встановіть: pip install firebase-admin"
            )
        except Exception as e:
            raise RuntimeError(f"Помилка підключення до Firebase: {e}")

    def _push(self, payload: Dict[str, Any]) -> bool:
        if not self.db:
            return False
        try:
            ref = self.db.reference(self.db_path)
            ref.push(payload)
            return True
        except Exception as e:
            print(f"❌ Помилка запису в Firebase: {e}")
            return False

    def output(self, message: str) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "text",
            "message": message,
        }
        self._push(payload)

    def output_dict(self, data: Dict[str, Any]) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "statistics",
            "data": data,
        }
        if self._push(payload):
            print(f"✅ Статистика записана в Firebase [{self.db_path}]: {data}")

    def output_list(self, items: List[str]) -> None:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "list",
            "items": items,
        }
        if self._push(payload):
            print(f"✅ Список записаний в Firebase ({len(items)} елементів)")

    def flush(self) -> None:
        """No persistent connection to close for Firebase Admin SDK."""
        print(f"✅ Firebase запис завершено (шлях: {self.db_path})")
