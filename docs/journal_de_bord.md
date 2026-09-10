# Journal de Bord

## 1. Fonctionnement du site
Le site est un catalogue public de 50 pages contenant chacune 20 livres. La page de liste ne donne pas d'identifiant unique (UPC) et affiche un faux stock générique. L'UPC et le stock exact ne sont disponibles qu'en ouvrant la fiche détaillée du produit.

## 2. Architecture
Le projet est organisé autour du concept de "Séparation des responsabilités" :
- `script/scraper/` : Ne gère QUE l'extraction HTTP et la lecture HTML.
- `script/utils/` : Ne gère QUE la base de données et le nettoyage des textes.
- `script/orchestrator.py` : Pilote le tout.
- L'Idempotence est garantie par Postgres (`ON CONFLICT DO NOTHING`) et la reprise sur erreur est gérée en vérifiant l'URL dans la BDD avant de requêter.

## 3. Données
Toutes les données sont formatées avant insertion :
- Prix : Convertis en nombres décimaux (`float`).
- Stock et Évaluations : Convertis en entiers (`int`).
- Catégories : Gérées dans une table SQL séparée pour éviter la redondance.

## 4. Problèmes principaux rencontrés
- **Récupérer le rating** : La note (1 à 5 étoiles) n'était pas textuelle. Elle était intégrée au nom de la classe CSS de la balise HTML (ex: `class="star-rating Three"`). J'ai créé un dictionnaire de mapping pour convertir ces mots en entier.
- **Récupérer le stock réel** : Le stock était affiché sous forme d'une phrase type `"In stock (22 available)"`. J'ai utilisé une Expression Régulière (Regex) pour capturer uniquement les chiffres présents avant le mot "available".
- **Reprise sur erreur** : Comment savoir si on a déjà scrapé un livre alors que l'UPC n'est pas sur la page liste ? J'ai utilisé l'URL du produit comme clé temporaire pour vérifier en base de données.
