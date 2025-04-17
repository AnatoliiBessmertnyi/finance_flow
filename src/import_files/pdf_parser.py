from datetime import datetime
import re
import pdfplumber


class TinkoffPDFParser:
    @staticmethod
    def parse(file_path: str):
        operations = []
        start_parsing = False
        current_operation = None

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                for line in text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue

                    if 'операции в валюте счёта' in line:
                        start_parsing = True
                        continue
                    if 'Операции по карте' in line:
                        start_parsing = False
                        if current_operation:
                            operations.append(current_operation)
                            current_operation = None
                        continue
                    if not start_parsing:
                        continue

                    if current_operation and not re.match(r'^\d{2}\.\d{2}\.\d{2}', line):
                        current_operation['description'] += ' ' + line
                        continue

                    date_match = re.match(r'^(\d{2}\.\d{2}\.\d{2}(?: \d{2}:\d{2})?)', line)
                    if not date_match:
                        if current_operation:
                            current_operation['description'] += ' ' + line
                        continue

                    if current_operation:
                        operations.append(current_operation)
                        current_operation = None

                    date_str = date_match.group(1)
                    remaining_line = line[date_match.end():].strip()

                    cleaned_line = re.sub(
                        r'^\d{2}\.\d{2}\.\d{2}', '', remaining_line
                    ).strip()

                    i_positions = [
                        m.start() for m in re.finditer(r'i', cleaned_line)
                    ]
                    if len(i_positions) < 2:
                        continue

                    last_i = i_positions[-1]
                    prev_i = i_positions[-2]
                    amount_part = cleaned_line[prev_i+1:last_i].strip()

                    amount_cleaned = amount_part.replace(' ', '').replace(
                        ',', '.'
                    )
                    if not amount_cleaned.startswith('+'):
                        amount_cleaned = '-' + amount_cleaned.lstrip('-')

                    try:
                        balance = float(amount_cleaned)
                    except ValueError:
                        continue

                    sum_start = cleaned_line.find(amount_part)
                    if sum_start == -1:
                        continue

                    description = cleaned_line[:sum_start].strip()
                    description = re.sub(r'\s*i\s*$', '', description)

                    current_operation = {
                        'date': (
                            datetime.strptime(date_str, '%d.%m.%y %H:%M')
                            if ':' in date_str
                            else datetime.strptime(
                                date_str + ' 00:00', '%d.%m.%y %H:%M'
                            )
                        ),
                        'description': description,
                        'balance': balance
                    }

        if current_operation:
            operations.append(current_operation)
        return operations
