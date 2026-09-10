from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.parse_utils import parse_rating, clean_price, extract_real_stock

def extract_list_page(html: str, base_url: str) -> tuple[list[str], str | None]:
    """
    Rôle : Analyser (parser) le HTML d'une page de LISTE.
    Ne fait aucune requête HTTP. Il se contente de lire le texte fourni et d'isoler les URLs.
    """
    soup = BeautifulSoup(html, 'html.parser')
    book_urls = []
    
    for article in soup.select('article.product_pod'):
        link = article.select_one('h3 a')
        if link and 'href' in link.attrs:
            # Reconstruire l'URL absolue
            absolute_url = urljoin(base_url, link['href'])
            book_urls.append(absolute_url)
            
    # Vérifie s'il y a une page suivante
    next_btn = soup.select_one('li.next a')
    next_page_url = urljoin(base_url, next_btn['href']) if next_btn else None
    
    return book_urls, next_page_url

def extract_book_details(html: str, source_url: str) -> dict:
    """
    Rôle : Analyser (parser) le HTML d'une FICHE PRODUIT détaillée.
    Retourne un dictionnaire standardisé prêt à être inséré en BDD.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Titre
    title_el = soup.select_one('div.product_main h1')
    title = title_el.text.strip() if title_el else ""
    
    # Description
    desc_el = soup.select_one('#product_description ~ p')
    description = desc_el.text.strip() if desc_el else ""
    
    # Catégorie (breadcrumb)
    breadcrumb = soup.select('ul.breadcrumb li a')
    category = breadcrumb[2].text.strip() if len(breadcrumb) >= 3 else ""
    
    # Note
    rating_el = soup.select_one('p.star-rating')
    rating = parse_rating(rating_el.get('class', [])) if rating_el else 0
    
    # Tableau d'informations (UPC, Prix, Stock, etc.)
    info_table = soup.select('table.table-striped tr')
    product_info = {}
    for row in info_table:
        th = row.select_one('th').text.strip()
        td = row.select_one('td').text.strip()
        product_info[th] = td
        
    return {
        'source_url': source_url,
        'title': title,
        'description': description,
        'category': category,
        'rating': rating,
        'upc': product_info.get('UPC', ''),
        'product_type': product_info.get('Product Type', ''),
        'price_excl_tax': clean_price(product_info.get('Price (excl. tax)', '0')),
        'price_incl_tax': clean_price(product_info.get('Price (incl. tax)', '0')),
        'tax': clean_price(product_info.get('Tax', '0')),
        'availability': product_info.get('Availability', ''),
        'real_stock': extract_real_stock(product_info.get('Availability', '')),
        'number_of_reviews': int(product_info.get('Number of reviews', '0'))
    }
