partie extract de scripts
parttie bdd postgres

Idée générale : boucle indempotente.

1) Extraction de la liste de tous les livres, extraite dans une bdd ou juste une variable ?
2) vérification des livres déjà présent dans la bdd via leur upc, on ne réinterroge que les livres non présents
3) itération sur chaque livre, récupération des données page par page
4) sauvegarde dans la bdd postgres tous les 50 livres (à faire évoluer), avec un fichier log qui trace
5) gestion des erreurs : chaque page peut échouer, une page ne pas faire échouer tout le projet
6) 
