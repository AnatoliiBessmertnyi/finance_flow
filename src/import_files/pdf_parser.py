from datetime import datetime
from typing import Dict, List

import pdfplumber


class TinkoffPDFParser:
    @staticmethod
    def parse(file_path: str) -> List[Dict]:
        operations = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                for line in text.split('\n'):
                    if "Дата и время операции:" in line:
                        parts = line.split()
                        date_str = parts[4]
                        time_str = parts[5] if len(parts) > 5 else "00:00"
                        description = " ".join(parts[6:-2])
                        amount = parts[-1]

                        operations.append({
                            "date": datetime.strptime(
                                f"{date_str} {time_str}", "%d.%m.%Y %H:%M"
                            ),
                            "description": description,
                            "amount": float(amount.replace(",", "."))
                        })
        return operations
