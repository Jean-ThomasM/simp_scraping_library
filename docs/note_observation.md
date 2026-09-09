# Note d'observation : Fiabilité des champs Prix et Taxes

Au cours de l'exploration des fiches produits sur `books.toscrape.com`, j'ai analysé en détail la structuration de la table d'informations (la balise `table.table-striped`), et plus spécifiquement les trois champs liés à la facturation : 
- `Price (excl. tax)` (Prix Hors Taxe)
- `Price (incl. tax)` (Prix Toutes Taxes Comprises)
- `Tax` (Montant de la taxe)

### Constatations empiriques
Après avoir scrapé un échantillon significatif du catalogue (et étendu ensuite à l'ensemble du jeu de données), j'ai constaté un comportement systématique sur l'intégralité des livres :
**Le montant de la taxe est invariablement de 0.00 £.**

Par conséquent, l'équation mathématique `Prix HT + Taxe = Prix TTC` est parfaitement respectée par le site, mais de manière "artificielle" : puisque `Tax = 0.00 £`, on retrouve systématiquement la même valeur (à l'arrondi près) pour le Prix HT et le Prix TTC (par exemple, 51.77 £ HT et 51.77 £ TTC). 

### Conclusion sur la fiabilité des champs
Bien que les données extraites soient techniquement consistantes (l'addition est correcte), **les champs liés à la fiscalité ne reflètent pas une réalité commerciale**. 

D'un point de vue "business" pour l'entreprise Bouquineo, on ne peut en aucun cas se fier au fait que le concurrent vend ses livres hors taxe à ses clients, car il s'agit très probablement d'un site "bac à sable" où la gestion complexe de la TVA (qui varie selon le type d'ouvrage et le pays de l'acheteur) n'a tout simplement pas été implémentée dans le backend de la plateforme.

Dans une application en production réelle, si la même anomalie était constatée, il faudrait impérativement :
1. Écarter l'analyse fiscale de ces données dans nos rapports commerciaux.
2. Ne conserver que le "Prix de vente public affiché" (ici le TTC) pour évaluer notre compétitivité.
