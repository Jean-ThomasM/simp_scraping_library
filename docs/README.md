# Projet Bouquineo - Scraper

## Résumé
Ce scraper collecte les données de 1000 livres depuis `books.toscrape.com`. Il extrait les informations cachées sur les fiches produits (UPC, stock réel, notation) et les sauvegarde de manière résiliente dans une base PostgreSQL.

## Principales commandes
Toutes les commandes Python doivent être lancées depuis la racine du projet.

1. **Démarrer l'environnement :**
   ```bash
   docker compose up -d
   uv sync
   ```
2. **Lancer le scraper complet :**
   ```bash
   uv run python script/main.py
   ```
3. **Lancer un test sur 5 livres :**
   ```bash
   uv run python script/main.py --sample 5
   ```
4. **Exporter le résultat en CSV :**
   ```bash
   uv run python script/export_csv.py
   ```
5. **Voir l'analyse des données (Pandas) :**
   ```bash
   uv run python script/analyze_pandas.py
   ```

## Comment se connecter à la BDD (DBeaver)
- **Hôte** : `localhost`
- **Port** : `5432`
- **Base de données** : `bouquineo`
- **Utilisateur** : `myuser`
- **Mot de passe** : `mypassword`

## Comment supprimer la BDD (et tout relancer)
Si vous souhaitez réinitialiser complètement la base de données pour forcer une nouvelle extraction complète :

1. Supprimez le conteneur et ses volumes de données persistants (`-v`) :
   ```bash
   docker compose down -v
   ```
2. Relancez une base de données totalement vierge (le script init.sql sera relu automatiquement) :
   ```bash
   docker compose up -d
   ```
