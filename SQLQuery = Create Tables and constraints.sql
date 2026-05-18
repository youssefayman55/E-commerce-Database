CREATE TABLE shop.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(150) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL 
        CHECK (role IN ('admin', 'customer', 'delivery')),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE shop.categories (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE shop.products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(150) NOT NULL,
    description NVARCHAR(MAX),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    category_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id)
        REFERENCES shop.categories(id)
);

CREATE TABLE shop.cart (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_cart_user
        FOREIGN KEY (user_id)
        REFERENCES shop.users(id)
);

CREATE TABLE shop.cart_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),

    CONSTRAINT fk_cart_items_cart
        FOREIGN KEY (cart_id)
        REFERENCES shop.cart(id),

    CONSTRAINT fk_cart_items_product
        FOREIGN KEY (product_id)
        REFERENCES shop.products(id)
);

CREATE TABLE shop.orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status NVARCHAR(20) NOT NULL 
        CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES shop.users(id)
);

CREATE TABLE shop.order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES shop.orders(id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES shop.products(id)
);

CREATE TABLE shop.payments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    method NVARCHAR(20) DEFAULT 'COD',
    status NVARCHAR(20) NOT NULL 
        CHECK (status IN ('pending', 'paid', 'failed')),
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES shop.orders(id)
);

CREATE TABLE shop.shipping (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    address NVARCHAR(MAX) NOT NULL,
    status NVARCHAR(20) NOT NULL 
        CHECK (status IN ('processing', 'shipped', 'delivered')),
    updated_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_shipping_order
        FOREIGN KEY (order_id)
        REFERENCES shop.orders(id)
);
