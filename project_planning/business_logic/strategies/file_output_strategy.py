import os
import json
from typing import Dict, Any, List
from datetime import datetime

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class FileOutputStrategy(IOutputStrategy):
    """
    Outputs messages to a file.
    Suitable for logging, audit trails, or offline processing.
    
    Configuration via environment variables:
      - OUTPUT_FILE_PATH: path to output file (default: output/log.jsonl)
    """

    def __init__(self, file_path: str = "output/log.jsonl"):
        """Initialize file output."""
        self.file_path = file_path
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Створена папка: {directory}")

    def _write_line(self, data: Dict[str, Any]) -> None:
        """Write a JSON line to the file."""
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            print(f"❌ Помилка запису у файл: {e}")

    def output(self, message: str) -> None:
        """Write a single message to file."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "type": "text",
        }
        self._write_line(payload)

    def output_dict(self, data: Dict[str, Any]) -> None:
        """Write a dictionary to file."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "statistics",
            "data": data,
        }
        self._write_line(payload)
        print(f"✅ Статистика записана у файл: {self.file_path}")

    def output_list(self, items: List[str]) -> None:
        """Write a list of items to file."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "type": "list",
            "items": items,
        }
        self._write_line(payload)
        print(f"✅ Список записаний у файл ({len(items)} елементів): {self.file_path}")

    def flush(self) -> None:
        """No-op for file output (already written)."""
        print(f"✅ Файл вихідних даних: {self.file_path}")
