import re

def parse_rating(class_list):
    """Convertit la classe CSS de la note (ex: ['star-rating', 'Three']) en entier."""
    mapping = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    for cls in class_list:
        if cls in mapping:
            return mapping[cls]
    return 0

def clean_price(price_str):
    """Extrait le nombre flottant d'une chaîne de prix (ex: '£51.77' -> 51.77)."""
    if not price_str:
        return 0.0
    match = re.search(r'[\d\.]+', price_str)
    if match:
        return float(match.group())
    return 0.0

def extract_real_stock(availability_str):
    """Extrait le stock réel de la chaîne (ex: 'In stock (22 available)' -> 22)."""
    if not availability_str:
        return 0
    match = re.search(r'\((\d+)\s+available\)', availability_str)
    if match:
        return int(match.group(1))
    # S'il y a juste écrit "In stock" sans nombre
    if 'in stock' in availability_str.lower():
        return 1
    return 0
