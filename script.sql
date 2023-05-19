CREATE TABLE IF NOT EXISTS "ITEM" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    stock INTEGER,
    price DECIMAL
);