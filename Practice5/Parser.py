import re

file_path = "practice5/raw.txt"

with open(file_path, encoding="utf-8") as file:
    data = file.read()

price_list = re.findall(r"Стоимость\s*\n([\d\s,]+)", data)

product_list = re.findall(r"\d+\.\s*\n(.+?)\n", data)

total_match = re.search(r"ИТОГО:\s*\n([\d\s,]+)", data)
total_value = total_match.group(1) if total_match else "Не найдено"

date_time_match = re.search(r"Время:\s*(.+)", data)
date_time = date_time_match.group(1) if date_time_match else "Не найдено"

payment = re.search(r"Банковская карта|Наличные", data)
payment_method = payment.group() if payment else "Не найдено"

print("Товары:")
for item in product_list:
    print("•", item)

print("\nЦены:")
for price in price_list:
    print("•", price)

print("\nИтого:", total_value)
print("Дата и время:", date_time)
print("Способ оплаты:", payment_method)
