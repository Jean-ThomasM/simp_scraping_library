# Flux d'exécution du Scraper Bouquineo

Voici le diagramme logique représentant la chaîne d'actions des différents scripts que nous avons créés :

```mermaid
flowchart TD
    %% Point d'entrée
    Start([Terminal : python main.py]) --> Config[Chargement config.py & .env]
    Config --> Orch[orchestrator.py]
    
    %% Phase 1
    subgraph Phase 1 : Collecte des URLs
        Orch -->|Itération sur les pages 1 à 50| Net1[network.py : get_page]
        Net1 --> Ext1[extract.py : extract_list_page]
        Ext1 -->|Concaténation| ListUrls[Liste brute de 1000 URLs]
    end
    
    %% Phase 2
    subgraph Phase 2 : Comparaison et Filtrage
        ListUrls --> CheckDB[db_utils.py : get_scraped_urls]
        CheckDB <-->|SELECT source_url| DB[(Base PostgreSQL\nDocker)]
        CheckDB -->|Filtrage| FilteredUrls[URLs non scrapées\n+ Application Mode Échantillon]
    end
    
    %% Phase 3
    subgraph Phase 3 : Extraction des détails
        FilteredUrls -->|Boucle URL par URL| Net2[network.py : get_page\n+ Temporisation 1.5s]
        Net2 --> Ext2[extract.py : extract_book_details]
        Ext2 --> Parse[parse_utils.py : Nettoyage\nStock, Prix, Notes CSS]
        Parse --> Save[db_utils.py : insert_book]
        Save -->|INSERT immédiat| DB
    end
    
    %% Export CSV
    subgraph Phase 4 : Export Livrable
        Export([Terminal : python export_csv.py]) --> Conn[db_utils.py : get_connection]
        Conn <-->|SELECT * JOIN categories| DB
        Conn --> CsvOut[\data/export_bouquineo.csv/]
    end

    %% Styles optionnels pour la lisibilité
    style Start fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff
    style Export fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style DB fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff
```

### Explications des étapes clés :

1. **Phase 1** : L'orchestrateur demande au réseau (`network.py`) de télécharger les pages de listes (de 1 à 50) et confie le code HTML à `extract.py` pour isoler uniquement les liens menant aux fiches produits.
2. **Phase 2 (La reprise sur erreur)** : Plutôt que de scraper aveuglément les 1000 liens, le script interroge la base de données. Il retire de sa liste toutes les fiches qui s'y trouvent déjà.
3. **Phase 3 (L'exécution sécurisée)** : Le script visite chaque livre manquant un par un, attend poliment 1,5 seconde, extrait toutes les données fines (UPC, stock réel, taxes), convertit les notes textuelles en chiffres avec `parse_utils.py`, et **sauvegarde immédiatement** en base pour ne rien perdre en cas de crash (coupure internet, arrêt manuel).
4. **Phase 4** : Action indépendante (à lancer en fin de projet) qui va lire la base de données finalisée pour générer le fichier CSV attendu par le jury.
