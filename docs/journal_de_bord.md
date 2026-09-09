# Journal de Bord

### Jour 1 : Matin - Cartographie et Analyse
- **Exploration du site cible** : Vérification du fichier `robots.txt` (qui est permissif et n'interdit pas le parcours du catalogue).
- **Problématique d'architecture** : J'ai remarqué que sur les pages de liste, on ne trouve que le titre raccourci, un prix et un niveau de stock basique ("In stock"). Il manque la clé primaire : le code UPC. L'UPC n'apparaît *que* sur les fiches produits.
- **Blocage & Résolution** : Comment savoir si j'ai déjà scrapé un livre si je n'ai pas l'UPC à l'avance ? J'ai décidé d'enregistrer l'URL source (`source_url`) comme clé unique dans ma base de données. Ainsi, je peux comparer les URLs trouvées sur la liste avec ma base avant de faire une requête HTTP inutile.

### Jour 1 : Après-midi - Scraper la liste
- Mise en place de `requests` et de `BeautifulSoup`.
- Mise en place du `User-Agent` (très important pour ne pas être vu comme un robot malveillant).
- **Blocage** : Les URLs récupérées étaient des chemins relatifs (`../../../a-light...`). 
- **Résolution** : Utilisation de `urllib.parse.urljoin` pour les reconstruire de manière robuste.

### Jour 2 : Matin - Fiches produits et formatage
- Écriture de la fonction d'extraction détaillée.
- **Défi de la Note (Rating)** : La note n'était pas écrite en texte, mais cachée dans une classe CSS (ex: `<p class="star-rating Three">`). 
- **Résolution** : Création d'une fonction utilitaire `parse_rating` avec un dictionnaire qui mappe `'One': 1`, `'Two': 2`, etc.
- **Défi du stock réel** : Le champ disponibilité ressemblait à "In stock (22 available)".
- **Résolution** : Utilisation d'une petite expression régulière (Regex) `r'\((\d+)\s+available\)'` pour extraire uniquement le "22" et le transformer en entier pour la base de données.

### Jour 2 : Après-midi - Persistance et Robustesse
- Création du `docker-compose.yml` avec PostgreSQL.
- **Blocage Python** : Lors de l'installation des dépendances (`psycopg2-binary`), une erreur de compilation C a bloqué l'installation à cause d'une incompatibilité avec la dernière version de Python (3.14).
- **Résolution** : Changement d'outil, passage à `psycopg` (version 3), qui est pure Python et supporte l'architecture la plus récente, ce qui a tout débloqué.
- Mise en place de l'orchestrateur. Test de la reprise sur interruption réussi grâce au stockage immédiat par itération (et non un stockage global à la fin). 
- Finition des tests et création du script d'export CSV.
