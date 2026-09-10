# Note d'observation

## Résumé des données
Notre scraper extrait un jeu de 1000 produits. La base de données contient le titre, la catégorie, le stock réel, l'identifiant unique (UPC), les prix HT/TTC, la taxe et la note.

## Analyse
Les champs extraits sont fiables à l'exception des variables de tarification. En effet, sur l'intégralité du catalogue, le champ `Tax` est systématiquement égal à `0.00 £`. 

## Réponse à la question du brief
*Question : "Sur quels titres le concurrent est-il en rupture ou en stock faible, et lesquels sont les mieux notés de son catalogue ?"*

**Réponse :** 
En interrogeant notre base de données (voir le script Pandas `analyze_pandas.py`), on constate qu'**aucun livre n'est en rupture de stock** sur ce site. Cependant, de nombreux livres ont un stock faible (1 ou 2 exemplaires).
Concernant les notes, on observe une répartition parfaite : environ 200 livres ont la note maximale de 5 étoiles, ce qui permet à la direction de Bouquineo de cibler l'analyse sur ces best-sellers.

*(L'autre enseignement majeur est mathématique : puisque la taxe est toujours de 0, le prix HT est systématiquement égal au prix TTC. Cette donnée est donc inutilisable pour une véritable analyse fiscale concurrentielle.)*
