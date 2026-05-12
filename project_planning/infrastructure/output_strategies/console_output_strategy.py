import json
from typing import Any

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class ConsoleOutputStrategy(IOutputStrategy):
    """Concrete strategy: serialises *data* and prints it to stdout."""

    def output(self, data: Any) -> None:
        if isinstance(data, (dict, list)):
            print(json.dumps(data, indent=2, default=str))
        else:
            print(data)
