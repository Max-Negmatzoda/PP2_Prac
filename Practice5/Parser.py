import re
import json


def clean_number(value):
    """Convert 1 200,00 → 1200.00"""
    return float(value.replace(" ", "").replace(",", "."))


def extract_prices(text):
    return re.findall(r'\d[\d\s]*,\d{2}', text)


def extract_product_names(text):
    pattern = re.compile(
        r'\d+\.\s*\n(.+?)\n[\d,\s]+\s*x',
        re.MULTILINE
    )
    return [m.group(1).strip() for m in pattern.finditer(text)]


def extract_items(text):
    items = []

    pattern = re.compile(
        r'\d+\.\s*\n'
        r'(.+?)\n'
        r'([\d,\s]+)\s*x\s*([\d\s,]+)\n'
        r'([\d\s,]+)',
        re.MULTILINE
    )

    for match in pattern.finditer(text):
        name = match.group(1).strip()
        quantity = clean_number(match.group(2))
        price = clean_number(match.group(3))
        total = clean_number(match.group(4))

        items.append({
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": total
        })

    return items


def extract_total(text):
    match = re.search(r'ИТОГО:\s*\n?\s*([\d\s]+,\d{2})', text)
    return clean_number(match.group(1)) if match else 0


def extract_datetime(text):
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
    if match:
        return match.group(1), match.group(2)
    return "", ""


def extract_payment_method(text):
    match = re.search(r'(Банковская карта|Наличные):', text)
    return match.group(1) if match else ""


def parse_receipt(text):
    items = extract_items(text)

    date, time = extract_datetime(text)

    return {
        "prices": extract_prices(text),
        "product_names": extract_product_names(text),
        "items": items,
        "calculated_total": sum(item["total"] for item in items),
        "receipt_total": extract_total(text),
        "date": date,
        "time": time,
        "payment_method": extract_payment_method(text)
    }


if __name__ == "__main__":
    with open("raw.txt", "r", encoding="utf-8") as file:
        text = file.read()

    result = parse_receipt(text)

    print(json.dumps(result, indent=4, ensure_ascii=False))
