-- Keyspace pour EcoStream
CREATE KEYSPACE IF NOT EXISTS ecostream
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE ecostream;

-- Table des événements bruts
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT,
    user_id INT,
    product_id INT,
    event_type TEXT,
    category TEXT,
    price DECIMAL,
    quantity INT,
    country TEXT,
    timestamp TIMESTAMP,
    PRIMARY KEY (event_id)
);

-- Index par utilisateur
CREATE INDEX IF NOT EXISTS idx_user ON events (user_id);

-- Index par produit
CREATE INDEX IF NOT EXISTS idx_product ON events (product_id);

-- Table des KPIs agrégés
CREATE TABLE IF NOT EXISTS kpis (
    product_id INT,
    date DATE,
    category TEXT,
    total_revenue DECIMAL,
    total_quantity INT,
    total_orders INT,
    cancel_rate DECIMAL,
    avg_price DECIMAL,
    PRIMARY KEY (product_id, date)
) WITH CLUSTERING ORDER BY (date DESC);

-- Table des prédictions d'abandon
CREATE TABLE IF NOT EXISTS predictions (
    user_id INT,
    timestamp TIMESTAMP,
    product_id INT,
    probability DECIMAL,
    level TEXT,
    PRIMARY KEY (user_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);