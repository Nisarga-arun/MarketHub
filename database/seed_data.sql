-- Sample seed data for testing.
-- User passwords: admin123, staff123, customer123 (hashed with Werkzeug)
-- Run after db_schema.sql
--
-- Required for UI tests (task.json): customer@example.com, categories

INSERT INTO db_test (message) VALUES ('Database connection successful');

INSERT INTO users (name, email, password_hash, role) VALUES
('Admin User', 'admin@example.com', 'pbkdf2:sha256:1000000$0Zb33kTzu0O7mwIr$aae79338d8ad81fd1da15eec415f4e75339980bcf621598269191b4f0b9baa44', 'admin'),
('Staff User', 'staff@example.com', 'pbkdf2:sha256:1000000$mrhXBintE1xw3LYR$66af4194bc673960cd5098b6b91581beae399b8c7edc30eceb2bddaf3594a915', 'staff'),
('Customer User', 'customer@example.com', 'pbkdf2:sha256:1000000$C0S9feW2c6NC6HPk$e49c106e63fa44d84528ee5f6a6a366fe2c052ca58d48237817d3a5e7ea25e1a', 'customer');

INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Apparel and fashion'),
('Books', 'Books and publications');

INSERT INTO stores (name, location) VALUES
('Sample Store', 'Main Street 1');

-- Assign staff@example.com (user_id=2) to Sample Store (store_id=1)
INSERT INTO store_staff (user_id, store_id, is_active) VALUES (2, 1, 1);

-- Seed products (store_id=1) with category_id for categories page
INSERT INTO products (store_id, category_id, name, description, price, quantity) VALUES
(1, 1, 'Seed Product', 'A product for editing', 10.00, 5),
(1, 1, 'Laptop', 'A laptop for work and play', 999.00, 5),
(1, 2, 'T-Shirt', 'Cotton t-shirt', 19.99, 20),
(1, 3, 'Headphones', 'Wireless headphones', 99.50, 10);

-- Pre-seeded order for staff UI test (customer user_id=3, product from store 1)
INSERT INTO orders (user_id, status) VALUES (3, 'placed');
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 1, 1, 10.00);
