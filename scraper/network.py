import requests
import time
import logging
from config import USER_AGENT, REQUEST_DELAY

def get_page(url, retries=3):
    """Télécharge une page web avec temporisation, User-Agent et retries."""
    headers = {
        'User-Agent': USER_AGENT
    }
    
    for attempt in range(retries):
        try:
            # Respect de la temporisation
            time.sleep(REQUEST_DELAY)
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.warning(f"Erreur lors de la requête vers {url} (Tentative {attempt + 1}/{retries}) : {e}")
            if attempt == retries - 1:
                logging.error(f"Échec définitif pour l'URL : {url}")
                return None
            time.sleep(REQUEST_DELAY * 2) # Backoff simple
    return None
