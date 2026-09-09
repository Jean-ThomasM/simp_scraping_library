import psycopg
import config
import logging

def get_connection():
    """Crée et retourne une connexion à la base de données."""
    return psycopg.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

def get_scraped_urls():
    """Récupère la liste des URLs déjà scrapées pour éviter les doublons."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT source_url FROM books;")
                records = cursor.fetchall()
                return {row[0] for row in records}
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des URLs : {e}")
        return set()

def insert_category(cursor, category_name):
    """Insère une catégorie si elle n'existe pas et retourne son ID."""
    cursor.execute(
        "INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (category_name,)
    )
    cursor.execute("SELECT id FROM categories WHERE name = %s;", (category_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_book(book_data):
    """Insère un livre dans la base de données."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cat_id = insert_category(cursor, book_data.get('category'))
                
                cursor.execute("""
                    INSERT INTO books (
                        upc, title, product_type, price_excl_tax, price_incl_tax, 
                        tax, availability, real_stock, number_of_reviews, rating, 
                        description, category_id, source_url
                    ) VALUES (
                        %(upc)s, %(title)s, %(product_type)s, %(price_excl_tax)s, %(price_incl_tax)s,
                        %(tax)s, %(availability)s, %(real_stock)s, %(number_of_reviews)s, %(rating)s,
                        %(description)s, %(category_id)s, %(source_url)s
                    ) ON CONFLICT (upc) DO NOTHING;
                """, {
                    **book_data,
                    'category_id': cat_id
                })
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion du livre {book_data.get('url')}: {e}")
        return False
