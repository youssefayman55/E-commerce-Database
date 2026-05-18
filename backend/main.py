from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# =========================================
# Database Connection
# =========================================

SERVER = "."
DATABASE = "E-CommerceDB"

connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&Encrypt=no"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================================
# FastAPI App
# =========================================

app = FastAPI()

# =========================================
# Models
# =========================================

class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class Product(BaseModel):
    name: str
    on: str
    pricdescriptie: float
    stock: int
    category_id: int


class Order(BaseModel):
    user_id: int
    total_price: float
    status: str


# =========================================
# Register User
# =========================================

@app.post("/register")
def register_user(user: UserRegister):

    try:
        with engine.connect() as conn:

            query = text("""
                INSERT INTO shop.users
                (name, email, password_hash, role)

                VALUES
                (:name, :email, :password, 'customer')
            """)

            conn.execute(query, {
                "name": user.name,
                "email": user.email,
                "password": user.password
            })

            conn.commit()

        return {"message": "User Registered Successfully"}

    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


# =========================================
# Get Products
# =========================================

@app.get("/products")
def get_products():

    try:
        with engine.connect() as conn:

            result = conn.execute(text("""
                SELECT 
                    p.id,
                    p.name,
                    p.description,
                    p.price,
                    p.stock,
                    c.name AS category
                FROM shop.products p
                JOIN shop.categories c ON p.category_id = c.id
                ORDER BY p.id
            """))

            products = []

            for row in result:
                products.append(dict(row._mapping))

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Add Product
# =========================================

@app.post("/add-product")
def add_product(product: Product):

    try:
        with engine.connect() as conn:

            conn.execute(text("""
                EXEC shop.sp_add_product
                    @name=:name,
                    @description=:description,
                    @price=:price,
                    @stock=:stock,
                    @category_id=:category_id
            """), {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category_id": product.category_id
            })

            conn.commit()

        return {"message": "Product Added"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Create Order
# =========================================

@app.post("/create-order")
def create_order(order: Order):

    try:
        with engine.connect() as conn:

            conn.execute(text("""
                EXEC shop.sp_add_order
                    @user_id=:user_id,
                    @total_price=:total_price,
                    @status=:status
            """), {
                "user_id": order.user_id,
                "total_price": order.total_price,
                "status": order.status
            })

            conn.commit()

        return {"message": "Order Created"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Get User Orders
# =========================================

@app.get("/user-orders/{user_id}")
def get_user_orders(user_id: int):

    try:
        with engine.connect() as conn:

            result = conn.execute(text("""
                EXEC shop.sp_get_user_orders
                    @user_id=:user_id
            """), {
                "user_id": user_id
            })

            orders = []

            for row in result:
                orders.append(dict(row._mapping))

        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Cancel Order
# =========================================

@app.put("/cancel-order/{order_id}")
def cancel_order(order_id: int):

    try:
        with engine.connect() as conn:

            conn.execute(text("""
                EXEC shop.sp_cancel_order
                    @order_id=:order_id
            """), {
                "order_id": order_id
            })

            conn.commit()

        return {"message": "Order Cancelled"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Top Selling Products
# =========================================

@app.get("/top-products")
def top_products():

    try:
        with engine.connect() as conn:

            result = conn.execute(text("""
                EXEC shop.sp_top_selling_products
            """))

            data = []

            for row in result:
                data.append(dict(row._mapping))

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Monthly Sales Report
# =========================================

@app.get("/sales-report")
def sales_report():

    try:
        with engine.connect() as conn:

            result = conn.execute(text("""
                EXEC shop.MonthlySalesReport
            """))

            data = []

            for row in result:
                data.append(dict(row._mapping))

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# Setup / Seed Database (Admin Only)
# =========================================

@app.post("/setup/seed-data")
def seed_database():
    """Insert sample data into the database"""
    try:
        with engine.connect() as conn:
            # Categories
            conn.execute(text("""
                INSERT INTO shop.categories (name) VALUES ('Electronics')
                INSERT INTO shop.categories (name) VALUES ('Fashion')
                INSERT INTO shop.categories (name) VALUES ('Books')
                INSERT INTO shop.categories (name) VALUES ('Home Appliances')
                INSERT INTO shop.categories (name) VALUES ('Sports')
            """))
            
            # Products
            conn.execute(text("""
                INSERT INTO shop.products (name, description, price, stock, category_id)
                VALUES 
                ('iPhone 15', 'Apple smartphone 128GB', 55000, 10, 1),
                ('Gaming Laptop', 'RTX gaming laptop', 42000, 5, 1),
                ('Running Shoes', 'Comfortable sport shoes', 1500, 20, 2),
                ('Clean Code Book', 'Programming best practices', 850, 15, 3),
                ('Air Fryer', 'Digital air fryer 5L', 3200, 8, 4),
                ('Football', 'Professional football', 700, 25, 5)
            """))
            
            conn.commit()
            return {"message": "Database seeded successfully"}
            
    except Exception as e:
        error_msg = str(e)
        if "UNIQUE constraint failed" in error_msg or "already exists" in error_msg:
            return {"message": "Data already exists"}
        raise HTTPException(status_code=500, detail=error_msg)