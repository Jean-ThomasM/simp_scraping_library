-- Initialisation de la base de données
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    upc VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    product_type VARCHAR(255),
    price_excl_tax DECIMAL(10, 2),
    price_incl_tax DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    availability VARCHAR(255),
    real_stock INTEGER,
    number_of_reviews INTEGER,
    rating INTEGER,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    source_url TEXT UNIQUE NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour la recherche rapide par URL (très utile pour vérifier ce qui est déjà scrapé)
CREATE INDEX IF NOT EXISTS idx_books_source_url ON books(source_url);
