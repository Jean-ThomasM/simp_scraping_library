# Plan d'Action : Projet de Scraping "Bouquineo"

Ce document décrypte les attentes de ton brief (`brief.md`) et structure le travail à faire, en expliquant *pourquoi* on fait les choses, et pas seulement *comment*.

## 1. Décryptage du Brief : Comprendre l'objectif

Avant de coder, il faut comprendre le besoin métier :
*   **Le Besoin :** Le client (Bouquineo) ne veut plus seulement la "vitrine" de son concurrent. Il veut savoir ce qu'il se passe en arrière-boutique : **sur quels livres le concurrent est-il en rupture de stock ? Quels sont les livres les mieux notés ?**
*   **Le Problème :** Ces informations ne sont pas sur les pages de liste, mais cachées dans les fiches produits individuelles.
*   **Le Vrai Défi :** Le volume. Scraper 1 page est facile. Scraper 1000 pages demande de la méthode. Si ton script plante au 900ème livre, tu ne veux pas recommencer à zéro. C'est ce qu'on appelle la **robustesse**.

### Les 4 pièges du brief à anticiper :
1.  **La note en CSS :** Tu ne chercheras pas un chiffre ("3/5"), mais tu devras extraire la classe CSS (ex: `class="star-rating Three"`) et la traduire en chiffre dans ton code Python.
2.  **Le faux stock :** La page liste dit "In stock". La fiche produit dit "In stock (22 available)". C'est ce "22" qu'on veut.
3.  **Les prix et taxes :** Tu vas voir des prix HT, TTC et des montants de taxes. **Astuce :** Regarde bien les valeurs sur le site, y a-t-il vraiment une différence entre HT et TTC ? Tu devras l'expliquer dans ta note d'observation.
4.  **L'UPC, le vrai identifiant :** Le titre d'un livre n'est pas unique (deux livres peuvent s'appeler "Poèmes"). L'UPC (Universal Product Code) est l'identifiant unique. C'est lui qui servira de "clé primaire" dans ta base de données.

---

## 2. Retour sur tes notes (`brouillon.md` et `architecture.md`)

Tes notes sont excellentes ! Tu as déjà fait ce qu'on appelle la "Phase de reconnaissance" (Phase 1 du brief).
*   Tu as compris la structure de pagination (`page-1.html`, `page-2.html`).
*   Tu as repéré comment récupérer l'URL de la fiche produit (le `<a href="...">` dans la page de liste).
*   Tu as repéré la structure tabulaire (`<table class="table table-striped">`) de la fiche produit, ce qui va grandement te faciliter l'extraction des données.
*   L'idée de "boucle idempotente" dans `architecture.md` est exactement ce qui est attendu pour la robustesse (Phase 2).

---

## 3. Plan d'Action Étape par Étape

### Jour 1 : Le "Carburant" (Reconnaissance et URLs)
*L'objectif d'aujourd'hui n'est pas la base de données ni le stock, mais de récupérer toutes les adresses des fiches.*

*   **Étape 1.1 : Préparation du script de liste**
    *   Crée un script Python (`scraper_listes.py`).
    *   Mets en place un `User-Agent` (le brief l'exige). C'est comme dire "Bonjour, je suis le bot de Jean-Thomas" au serveur.
    *   Mets en place une pause (`time.sleep()`) entre les requêtes.
*   **Étape 1.2 : Scraper les 50 pages de listes**
    *   Fais une boucle de 1 à 50 pour générer les URLs des pages de catalogue.
    *   Pour chaque livre de la page, extrais : Titre, Prix (celui affiché), Note (traduis "Three" en 3), et **surtout l'URL relative de la fiche produit**.
*   **Étape 1.3 : Reconstruire l'URL absolue**
    *   L'URL récupérée sera relative (ex: `a-light-in-the-attic_1000/index.html`). Tu dois la concaténer avec la base (`https://books.toscrape.com/catalogue/`) pour qu'elle soit utilisable demain.
*   **Étape 1.4 : Sauvegarde temporaire**
    *   Sauvegarde ces 1000 résultats (avec leur URL complète) dans un fichier `livres_urls.csv` ou un fichier `.json`.
    *   *Fin du J1 : Tu as 1000 URLs prêtes à être visitées.*

### Jour 2 : L'Exploration Profonde et la Base de Données
*L'objectif est d'aller chercher le stock sur les 1000 fiches produits, de manière robuste.*

*   **Étape 2.1 : Mise en place de PostgreSQL**
    *   Lance un container Docker PostgreSQL.
    *   Écris un script SQL (`init_db.sql`) pour créer ta table `livres`. **Mets l'UPC en `PRIMARY KEY`**.
*   **Étape 2.2 : Le script de fiches produits (Mode Échantillon)**
    *   Crée un nouveau script (`scraper_fiches.py`).
    *   Ajoute un paramètre (ou une variable) `LIMITE = 10` pour ne tester que sur 10 livres au début.
    *   Ouvre ton fichier `livres_urls.csv`, et pour chaque URL, va requêter la page.
*   **Étape 2.3 : Extraction des données manquantes**
    *   Dans la page, extrais : l'UPC, le stock réel (isole le chiffre de la chaîne "In stock (22 available)"), les prix détaillés, le nombre d'avis, etc.
*   **Étape 2.4 : La Robustesse (Le cœur du sujet)**
    *   **Gestion des erreurs :** Entoure ton code de scraping d'un bloc `try... except`. Si une page renvoie une erreur 404 ou 500, log l'erreur (avec le module `logging`), et fais un `continue` pour passer au livre suivant sans crasher le script.
    *   **Idempotence :** Avant de scaper une URL, peux-tu vérifier si l'UPC ou l'URL est déjà dans ta base PostgreSQL ?
        *   *Méthode 1 :* Ton scraper fait un `SELECT` en base. Si le livre existe, il passe au suivant (pas de requête HTTP). S'il n'existe pas, il le scrape.
        *   *Méthode 2 :* Tu insères chaque livre au fur et à mesure (et pas les 1000 d'un coup à la fin). Si le script plante au 700ème, au prochain lancement, les 700 premiers seront détectés comme "déjà en base" et seront ignorés.
*   **Étape 2.5 : Validation et Livraison**
    *   Passe le script en mode complet (1000 livres).
    *   Rédige le `README.md` avec les instructions pour lancer la BDD Docker et tes scripts.
    *   Rédige ton journal de bord.

---

## 💡 Le point sur lequel se concentrer en premier :
Commence par te créer un environnement virtuel Python propre et crée un petit fichier de test pour extraire correctement la note (les étoiles) de la page HTML. C'est souvent le premier petit obstacle technique.
