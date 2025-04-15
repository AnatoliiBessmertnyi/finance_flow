from datetime import datetime
import re
import pdfplumber


class TinkoffPDFParser:
    @staticmethod
    def parse(file_path: str):
        start_parsing = False
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                for line in text.split('\n'):
                    print()
                    print('LINE:', line)

                    if 'операции в валюте счёта' in line:
                        start_parsing = True
                        continue
                    if 'Операции по карте' in line:
                        start_parsing = False
                        continue
                    if not start_parsing:
                        continue

                    date_match = re.match(
                        r'^(?P<date>\d{2}\.\d{2}\.\d{2}(?: \d{2}:\d{2})?)', line
                    )

                    if not date_match:
                        continue

                    date_str = date_match.group('date')
                    remaining_line = line[date_match.end():].strip()
                    cleaned_line = re.sub(
                        r'^\d{2}\.\d{2}\.\d{2}', '', remaining_line
                    ).strip()
                    print('date_str', date_str)
                    print('cleaned_line', cleaned_line)

                    i_positions = [m.start() for m in re.finditer(r'i', cleaned_line)]
                    last_i = i_positions[-1]
                    prev_i = i_positions[-2]
                    amount_part = cleaned_line[prev_i+1:last_i].strip()
                    amount_cleaned = amount_part.replace(' ', '')
                    amount_cleaned = amount_cleaned.replace(',', '.')
                    if '+' not in amount_cleaned:
                        amount_cleaned = '-' + amount_cleaned.lstrip('-')
                    print(amount_cleaned)

                    sum_start = cleaned_line.find(amount_part)
                    description = cleaned_line[:sum_start].strip()
                    print(description)
