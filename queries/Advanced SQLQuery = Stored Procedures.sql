-- 1th Stored Procedure (Add Order)

create procedure shop.sp_add_order 
@user_id int ,
@total_price decimal(10,2),
@status nvarchar(20)

as
begin
	set nocount on ;

	insert into shop.orders 
	(user_id  , total_price , status , created_at)

	values 
	(@user_id , @total_price,@status,getdate());

    print 'Order Added Successfully'
end;

exec shop.sp_add_order 
	@user_id = 2 ,
	@total_price = 5900,
	@status = 'pending' ;

select * from shop.orders;


-------------------------------------------
-------------------------------------------

-- 2th Stored Procedure (UpdateStock)
create procedure shop.sp_update_stock

	@product_id int , 
	@new_stock int 
as 
begin
    set nocount on;

	update shop.products 
	set stock = @new_stock

	where id = @product_id

end ;

exec shop.sp_update_stock 
	@product_id = 1 ,
	@new_stock = 37 ;

select * from shop.products;


---------------------------------------
---------------------------------------

-- 3th Stored Procedure (Get User Orders)
create procedure shop.sp_get_user_orders 

     @user_id int 
as 
begin 
     set nocount on ;

	 select 
	    o.id as order_id,
		o.total_price ,
		o.status , 
		o.created_at 
	from shop.orders o
	where o.user_id = @user_id

	order by o.created_at desc ;

end;

exec shop.sp_get_user_orders @user_id = 2 ;

select * from shop.orders;


-----------------------------------------------
-----------------------------------------------

-- 4th Stored Procedure (Cancel Order)
create procedure shop.sp_cancel_order
    @order_id int 
as 
begin 
    set nocount on ;

	update shop.orders 
	set status = 'cancelled'

	where shop.orders.id = @order_id;

	print 'Oredr Cancelled Successfully'
end;

exec shop.sp_cancel_order @order_id = 3 ;

select * from shop.orders;


---------------------------------------------
---------------------------------------------

-- 5th Stored Procedure (Add Product)
create procedure shop.sp_add_product

	@name nvarchar(150) ,
	@description nvarchar(max),
	@price decimal(10,2),
	@stock int ,
	@category_id int 
as
begin 
    set nocount on ;

	insert into shop.products 
	(name,description,price,stock,category_id)
	
	values
	(@name,@description,@price,@stock,@category_id)

	print 'Your Product Added Successfully' 
end ;


exec shop.sp_add_product 
    @name = 'Wireless Mouse',
    @description = 'Gaming wireless mouse',
    @price = 1200,
    @stock = 15,
    @category_id = 1;
	

select * from shop.products ;

------------------------------------------------
------------------------------------------------

-- 6th Stored procedure (Top Selling Products)
create procedure shop.sp_top_selling_products
as
begin 
    set nocount on ;

	select  
		top 10 
		p.name ,
		sum(oi.quantity) as total_sold

	from shop.order_items  oi

	join shop.products p
	on oi.product_id = p.id

	group by p.name 
	
	order by total_sold desc 
end ;


exec shop.sp_top_selling_products;

select * from shop.products;


--------------------------------------------
--------------------------------------------

-- 7th Stroed Procedure (Monthly Sales Report)
CREATE PROCEDURE shop.MonthlySalesReport
AS
BEGIN

    SET NOCOUNT ON;

    SELECT

        YEAR(created_at) AS year,

        MONTH(created_at) AS month,

        SUM(total_price) AS total_sales,

        COUNT(*) AS total_orders

    FROM shop.orders

    WHERE status != 'cancelled'

    GROUP BY
        YEAR(created_at),
        MONTH(created_at)

    ORDER BY
        year DESC,
        month DESC;

END;

EXEC shop.MonthlySalesReport;