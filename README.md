# Projet Bouquineo - Scraper de la librairie concurrente

## 1. Description du Projet
Ce projet est un scraper conçu pour collecter les informations de 1 000 livres depuis le catalogue du libraire concurrent (books.toscrape.com), sans protection anti-robot mais avec les mêmes exigences de fiabilité qu'en environnement de production. L'objectif est de répondre à des problématiques commerciales précises (niveau de stock, évaluations, et gestion des UPCs).

## 2. Choix Techniques et Justifications
*   **Python (BeautifulSoup + Requests)** : Le site cible est intégralement en HTML statique. Il n'y avait donc aucune nécessité de charger un navigateur complet (Selenium/Playwright) qui aurait considérablement ralenti l'exécution.
*   **PostgreSQL (via Docker)** : La donnée est structurée. Une base relationnelle permet d'isoler les catégories, de garantir l'unicité de chaque UPC et d'empêcher les doublons. Docker permet une portabilité absolue.
*   **Bibliothèque `psycopg` (v3)** : Utilisée au lieu de l'historique `psycopg2` pour s'assurer d'une compatibilité parfaite avec les versions très récentes de Python.
*   **Temporisation & User-Agent** : Une temporisation (1.5s par défaut) est implémentée avec la bibliothèque `time`. Le User-Agent est explicitement renseigné dans les variables d'environnement (`Bouquineo_Bot/1.0 (+contact@bouquineo.fr)`). Le rythme garantit l'intégrité du serveur cible.
*   **Robustesse (Reprise sur erreur)** : Pour être sûr de pouvoir reprendre le scraping exactement là où il a été interrompu, le scraper compare la liste des URLs récupérées sur les listes avec les URLs déjà enregistrées en base de données. Les requêtes unitaires sur les fiches de livres déjà collectés sont ainsi totalement ignorées.

## 3. Installation et Lancement depuis zéro

### Prérequis
*   Docker (pour PostgreSQL)
*   Python 3.10 ou supérieur

### Mise en place
1. Clonez ce dépôt.
2. Démarrez la base de données :
   ```bash
   docker compose up -d
   ```
3. Créez l'environnement virtuel et installez les dépendances :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Initialisez le fichier `.env` :
   ```bash
   cp .env.example .env
   ```

### Lancement du Scraper
Pour lancer le scraper complet (pensez à passer `MODE=prod` dans le `.env` pour faire les 1000) :
```bash
python main.py
```

**Mode Échantillon (Démonstration)**
Pour limiter l'exécution, vous pouvez utiliser l'argument CLI :
```bash
python main.py --sample 5
```

### Export des données en CSV
Une fois le scraping terminé (ou partiel), vous pouvez générer le livrable CSV :
```bash
python export_csv.py
```
Le fichier `export_bouquineo.csv` sera créé dans le dossier `data/`.

## 4. Auteur
Créé dans le cadre d'un mini-brief de développement pour l'architecture et l'extraction de données.
