import logging
import config
from scraper.network import get_page
from scraper.extract import extract_list_page, extract_book_details
from utils.db_utils import get_scraped_urls, insert_book

def run_orchestrator(sample_size=None):
    logging.info("Démarrage de l'orchestrateur...")
    
    base_url = config.BASE_URL
    current_url = f"{base_url}/catalogue/page-1.html"
    
    # 1. Récupération des URLs des fiches produits
    all_book_urls = []
    page_count = 0
    
    logging.info("--- Phase 1 : Collecte des URLs ---")
    while current_url and page_count < config.MAX_PAGES:
        logging.info(f"Parcours de la liste : {current_url}")
        html = get_page(current_url)
        if not html:
            break
            
        urls, next_url = extract_list_page(html, current_url)
        all_book_urls.extend(urls)
        
        current_url = next_url
        page_count += 1
        
    logging.info(f"{len(all_book_urls)} URLs de livres collectées sur {page_count} pages de liste.")
    
    # 2. Comparaison avec la base de données
    logging.info("--- Phase 2 : Comparaison avec la base de données ---")
    scraped_urls = get_scraped_urls()
    logging.info(f"{len(scraped_urls)} livres déjà présents en base de données.")
    
    urls_to_scrape = [url for url in all_book_urls if url not in scraped_urls]
    logging.info(f"Il reste {len(urls_to_scrape)} fiches produits à extraire.")
    
    # Mode échantillon
    if sample_size and sample_size > 0:
        urls_to_scrape = urls_to_scrape[:sample_size]
        logging.info(f"Mode échantillon activé : restriction à {sample_size} fiches produits.")

    # 3. Collecte des fiches produits et sauvegarde
    logging.info("--- Phase 3 : Extraction des détails et sauvegarde ---")
    success_count = 0
    error_count = 0
    
    for i, url in enumerate(urls_to_scrape):
        logging.info(f"Extraction ({i+1}/{len(urls_to_scrape)}) : {url}")
        html = get_page(url)
        
        if not html:
            error_count += 1
            logging.error(f"Impossible de récupérer la page : {url}")
            continue
            
        try:
            book_data = extract_book_details(html, url)
            
            # Sauvegarde immédiate en base de données
            if insert_book(book_data):
                success_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            error_count += 1
            logging.error(f"Erreur inattendue lors de l'extraction de {url} : {e}")
            
    logging.info("--- Fin de l'extraction ---")
    logging.info(f"Succès : {success_count} | Erreurs : {error_count}")
