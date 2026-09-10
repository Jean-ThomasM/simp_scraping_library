import requests
import time
import logging
from config import USER_AGENT, REQUEST_DELAY

def get_page(url: str, retries: int = 3) -> str | None:
    """
    Rôle : Gérer les requêtes HTTP (Le "Facteur").
    Il ne sait rien du HTML ni de la BDD. Son seul rôle est d'aller chercher le texte brut d'une page.
    
    Args:
        url: L'adresse web à télécharger.
        retries: Le nombre de tentatives en cas d'échec de connexion.
    """
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
