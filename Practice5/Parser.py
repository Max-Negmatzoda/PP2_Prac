import re
import json

file_path = "practice5/raw.txt"

with open(file_path, encoding="utf-8") as file:
    data = file.read()

price_list = re.findall(r"Стоимость\s*\n([\d\s,]+)", data)
product_list = re.findall(r"\d+\.\s*\n(.+?)\n", data)

total_match = re.search(r"ИТОГО:\s*\n([\d\s,]+)", data)
total_value = total_match.group(1) if total_match else None

date_time_match = re.search(r"Время:\s*(.+)", data)
date_time = date_time_match.group(1) if date_time_match else None

payment = re.search(r"Банковская карта|Наличные", data)
payment_method = payment.group() if payment else None

result = {
    "products": product_list,
    "prices": price_list,
    "total": total_value,
    "date_time": date_time,
    "payment_method": payment_method
}

print(json.dumps(result, indent=4, ensure_ascii=False))
