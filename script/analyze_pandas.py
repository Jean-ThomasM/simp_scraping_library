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
                        b.title, 
                        c.name as category, 
                        b.real_stock, 
                        b.rating, 
                        b.price_excl_tax
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                """)
                records = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]

        # Création du DataFrame Pandas
        df = pd.DataFrame(records, columns=col_names)

        print("\n--- ANALYSE DES DONNÉES BOUQUINEO ---\n")
        
        print(f"Nombre total de livres en base : {len(df)}")
        
        if len(df) == 0:
            print("Aucune donnée à analyser. Veuillez lancer le scraper d'abord.")
            return

        print("\n1. Répartition des notes (Rating) :")
        print(df['rating'].value_counts().sort_index(ascending=False).to_string())

        print("\n2. Statistiques sur le stock :")
        print(f"- Stock moyen : {df['real_stock'].mean():.1f} exemplaires")
        print(f"- Stock maximum : {df['real_stock'].max()} exemplaires")
        print(f"- Nombre de livres en rupture de stock (0) : {len(df[df['real_stock'] == 0])}")
        print(f"- Nombre de livres en stock faible (<= 3) : {len(df[df['real_stock'] <= 3])}")

        print("\n3. Les 5 livres les plus chers :")
        top_expensive = df.sort_values(by='price_excl_tax', ascending=False).head(5)
        print(top_expensive[['title', 'price_excl_tax']].to_string(index=False))

    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")

if __name__ == "__main__":
    analyze_data()
