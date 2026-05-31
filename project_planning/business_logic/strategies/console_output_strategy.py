import json
from typing import Dict, Any, List

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class ConsoleOutputStrategy(IOutputStrategy):
    """
    Outputs messages to stdout (console).
    Simple, human-readable format for development and testing.
    """

    def output(self, message: str) -> None:
        """Print a single message to console."""
        print(message)

    def output_dict(self, data: Dict[str, Any]) -> None:
        """Print a dictionary with formatted output."""
        print("\n" + "=" * 60)
        print("📊 Статистика імпорту:")
        print("=" * 60)
        for key, value in data.items():
            print(f"  {key.capitalize()}: {value}")
        print("=" * 60 + "\n")

    def output_list(self, items: List[str]) -> None:
        """Print a list of items."""
        print("\n📋 Список елементів:")
        for idx, item in enumerate(items, 1):
            print(f"  {idx}. {item}")
        print()

    def flush(self) -> None:
        """No-op for console output."""
        pass
