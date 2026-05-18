INSERT INTO shop.categories (name)
VALUES
('Electronics'),
('Fashion'),
('Books'),
('Home Appliances'),
('Sports');


INSERT INTO shop.users (name, email, password_hash, role)
VALUES
('Admin User', 'admin@shop.com', 'hashed_admin_pass', 'admin'),

('Ahmed Ali', 'ahmed@gmail.com', 'hashed_pass_1', 'customer'),

('Sara Mohamed', 'sara@gmail.com', 'hashed_pass_2', 'customer'),

('Delivery User', 'delivery@shop.com', 'hashed_delivery', 'delivery');


INSERT INTO shop.products
(name, description, price, stock, category_id)
VALUES

('iPhone 15',
'Apple smartphone 128GB',
55000,
10,
1),

('Gaming Laptop',
'RTX gaming laptop',
42000,
5,
1),

('Running Shoes',
'Comfortable sport shoes',
1500,
20,
2),

('Clean Code Book',
'Programming best practices',
850,
15,
3),

('Air Fryer',
'Digital air fryer 5L',
3200,
8,
4),

('Football',
'Professional football',
700,
25,
5);

INSERT INTO shop.cart (user_id)
VALUES
(2),
(3);


INSERT INTO shop.cart_items
(cart_id, product_id, quantity)
VALUES
(1, 1, 1),
(1, 4, 2),
(2, 3, 1),
(2, 6, 3);


INSERT INTO shop.orders
(user_id, total_price, status)
VALUES
(2, 55850, 'pending'),
(3, 3600, 'shipped');


INSERT INTO shop.order_items
(order_id, product_id, quantity, price)
VALUES
(1, 1, 1, 55000),
(1, 4, 1, 850),
(2, 5, 1, 3200),
(2, 6, 1, 400);



INSERT INTO shop.payments
(order_id, amount, method, status)
VALUES
(1, 55850, 'COD', 'pending'),
(2, 3600, 'COD', 'paid');

INSERT INTO shop.shipping
(order_id, address, status)
VALUES

(1,
'Beni Suef, Egypt',
'processing'),

(2,
'Cairo, Egypt',
'shipped');


SELECT * FROM shop.products;

SELECT 
    o.id AS order_id,
    u.name AS customer_name,
    o.total_price,
    o.status
FROM shop.orders o
JOIN shop.users u
ON o.user_id = u.id;

SELECT
    o.id AS order_id,
    p.name AS product_name,
    oi.quantity,
    oi.price
FROM shop.order_items oi
JOIN shop.orders o
ON oi.order_id = o.id
JOIN shop.products p
ON oi.product_id = p.id;