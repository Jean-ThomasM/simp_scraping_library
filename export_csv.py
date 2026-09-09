import csv
import logging
from utils.db_utils import get_connection

def export_to_csv(output_file='data/export_bouquineo.csv'):
    """Exporte le contenu de la table books vers un fichier CSV."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Requête avec jointure pour récupérer le nom de la catégorie au lieu de son ID
                cursor.execute("""
                    SELECT 
                        b.upc, b.title, b.product_type, b.price_excl_tax, 
                        b.price_incl_tax, b.tax, b.availability, b.real_stock, 
                        b.number_of_reviews, b.rating, c.name as category, 
                        b.source_url, b.description
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                """)
                records = cursor.fetchall()
                
                # Noms des colonnes (headers)
                col_names = [desc[0] for desc in cursor.description]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerows(records)
            
        logging.info(f"Export réussi : {len(records)} livres exportés dans {output_file}")
        
    except Exception as e:
        logging.error(f"Erreur lors de l'export CSV : {e}")

if __name__ == "__main__":
    export_to_csv()
