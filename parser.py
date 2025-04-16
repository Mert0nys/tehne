import requests
from lxml import html
import re

def parse_price(url, xpath):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к URL {url}: {e}")

    tree = html.fromstring(response.content)

    price_elements = tree.xpath(xpath)
    if not price_elements:
        raise ValueError(f"Элемент не найден по XPath: {xpath}")

    for elem in price_elements:
        print(f"Найден элемент: '{elem.text_content().strip()}'")

    price_string = price_elements[0].text_content().strip()

    print(f"Полученная строка с ценой: '{price_string}'")

    price_string = price_string.replace(" ", "").replace("₽", "").replace("$", "").replace("€", "").replace(",", ".")

    price_string = ''.join(c for c in price_string if c.isdigit() or c == '.')
    
    if not price_string:
        raise ValueError(f"Строка не содержит допустимых чисел: {price_string}")

    try:
        return float(price_string)
    except ValueError:
        raise ValueError(f"Не удалось преобразовать цену: {price_string}")

