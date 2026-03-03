-- Migration: add unit_id to sales_agreement_items with data backfill
-- Usage (SQLite): sqlite3 db.sqlite3 < migrations/002_add_unit_to_sales_agreement_items.sql

PRAGMA foreign_keys=off;

CREATE TABLE sales_agreement_items_new (
    id INTEGER PRIMARY KEY,
    agreement_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (agreement_id) REFERENCES sales_agreements (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (unit_id) REFERENCES units (id)
);

INSERT INTO sales_agreement_items_new (id, agreement_id, product_id, unit_id, quantity, price)
SELECT
    sai.id,
    sai.agreement_id,
    sai.product_id,
    (SELECT p.unit_id FROM products p WHERE p.id = sai.product_id) AS unit_id,
    sai.quantity,
    sai.price
FROM sales_agreement_items sai;

DROP TABLE sales_agreement_items;
ALTER TABLE sales_agreement_items_new RENAME TO sales_agreement_items;

PRAGMA foreign_keys=on;
