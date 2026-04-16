import csv
from typing import List, Dict
from data_access.interfaces.i_csv_reader import ICsvReader


class CsvReader(ICsvReader):
    """Reads a multi-entity CSV file and returns list of row dicts."""

    def read(self, file_path: str) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows
