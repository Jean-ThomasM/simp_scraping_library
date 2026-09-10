import os
from pathlib import Path
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env à la racine
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration Scraping
BASE_URL = os.getenv("BASE_URL", "https://books.toscrape.com")
MAX_PAGES = int(os.getenv("MAX_PAGES", 50))
MODE = os.getenv("MODE", "test").lower()
SAMPLE_SIZE = int(os.getenv("SAMPLE_SIZE", 20))

# Configuration Réseau
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible; BouquineoBot/1.0)")
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 1.0))

# Configuration Base de données
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "bouquineo")
DB_USER = os.getenv("POSTGRES_USER", "myuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
