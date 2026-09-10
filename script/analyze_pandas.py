import pandas as pd
from utils.db_utils import get_connection

def analyze_data():
    print("Connexion à la base de données...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Requête pour récupérer toutes les données utiles
                cursor.execute("""
                    SELECT 
                        b.upc, b.title, c.name as category, 
                        b.real_stock, b.rating, 
                        b.price_excl_tax, b.price_incl_tax, b.tax,
                        b.number_of_reviews, b.description
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                """)
                records = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]

        # Création du DataFrame Pandas
        # On force la conversion numérique sur les colonnes qui pourraient arriver en Decimal depuis la BDD
        df = pd.DataFrame(records, columns=col_names)
        for col in ['price_excl_tax', 'price_incl_tax', 'tax']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        print("\n--- ANALYSE DES DONNÉES BOUQUINEO ---\n")
        
        print(f"Nombre total de livres en base : {len(df)}")
        
        if len(df) == 0:
            print("Aucune donnée à analyser. Veuillez lancer le scraper d'abord.")
            return

        print("\n1. Qualité des données (Valeurs manquantes ou vides) :")
        # On compte les nulls et les chaînes vides
        missing_or_empty = df.isnull().sum() + (df == "").sum()
        if missing_or_empty.sum() == 0:
            print("-> Excellente : Aucun champ manquant détecté sur l'ensemble du catalogue.")
        else:
            print("-> Champs présentant globalement des données manquantes :")
            print(missing_or_empty[missing_or_empty > 0].to_string())
            
            print("\n-> Détail des livres concernés :")
            # Masque pour trouver les lignes ayant au moins un NaN ou un champ vide
            mask = df.isnull().any(axis=1) | (df == "").any(axis=1)
            missing_rows = df[mask]
            
            for _, row in missing_rows.iterrows():
                # On identifie la ou les colonnes précises qui posent problème pour cette ligne
                cols = [col for col in df.columns if pd.isna(row[col]) or row[col] == ""]
                print(f"   - Titre : \"{row['title']}\" (UPC: {row['upc']}) -> Manque : {', '.join(cols)}")

        print("\n2. Variations Statistiques (Min, Médiane, Max, Moyenne) :")
        num_cols = ['real_stock', 'rating', 'price_excl_tax', 'price_incl_tax', 'tax', 'number_of_reviews']
        stats = df[num_cols].agg(['min', 'median', 'max', 'mean']).T
        stats.columns = ['Minimum', 'Médiane', 'Maximum', 'Moyenne']
        # Arrondir la moyenne pour un affichage propre
        stats['Moyenne'] = stats['Moyenne'].round(2)
        print(stats.to_string())

        print("\n3. Répartition des notes (Rating) :")
        print(df['rating'].value_counts().sort_index(ascending=False).to_string())

        print("\n4. Les 5 livres les plus chers (HT) :")
        top_expensive = df.sort_values(by='price_excl_tax', ascending=False).head(5)
        print(top_expensive[['title', 'price_excl_tax']].to_string(index=False))

    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    analyze_data()
