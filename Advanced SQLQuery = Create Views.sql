-- view about all orders in the database 
CREATE VIEW shop.v_order_summary AS
SELECT
    o.id AS order_id,
    u.name AS customer_name,
    o.total_price,
    o.status,
    o.created_at
FROM shop.orders o
JOIN shop.users u
ON o.user_id = u.id;

select * from shop.v_order_summary;


---------------------------------------------
---------------------------------------------


-- view about all products in the database 
CREATE VIEW shop.v_product_inventory AS
SELECT 
     p.id ,
     p.name ,
     c.name AS category ,
     p.price ,
     p.stock 
FROM shop.products p 
JOIN shop.categories c
ON p.category_id = c.id;

select * from shop.v_product_inventory;



-----------------------------------------------
-----------------------------------------------


-- view about all payment methods 
create view shop.v_payments_methods as 
select 
o.id as order_id ,
p.amount as total_price, 
p.method ,
p.status ,
p.created_at 

from shop.orders o 
join shop.payments p
on o.id = p.order_id;

select * from shop.v_payments_methods;