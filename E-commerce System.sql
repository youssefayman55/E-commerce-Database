CREATE TABLE [users] (
  [user_id] int PRIMARY KEY IDENTITY(1, 1),
  [user_name] nvarchar(255),
  [email] nvarchar(255) UNIQUE,
  [password] nvarchar(255),
  [role] nvarchar(255),
  [created_at] datetime
)
GO

CREATE TABLE [categories] (
  [cat_id] int PRIMARY KEY IDENTITY(1, 1),
  [cat_name] nvarchar(255)
)
GO

CREATE TABLE [products] (
  [product_id] int PRIMARY KEY IDENTITY(1, 1),
  [product_name] nvarchar(255),
  [description] text,
  [price] decimal,
  [stock] int,
  [cat_id] int,
  [created_at] datetime
)
GO

CREATE TABLE [cart] (
  [cart_id] int PRIMARY KEY IDENTITY(1, 1),
  [user_id] int UNIQUE,
  [created_at] datetime
)
GO

CREATE TABLE [cart_item] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [cart_id] int,
  [product_id] int,
  [quantity] int
)
GO

CREATE TABLE [orders] (
  [order_id] int PRIMARY KEY IDENTITY(1, 1),
  [user_id] int,
  [total_price] decimal,
  [status] nvarchar(255),
  [created_at] datetime
)
GO

CREATE TABLE [order_item] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [order_id] int,
  [product_id] int,
  [quantity] int,
  [price] deciaml
)
GO

CREATE TABLE [payments] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [order_id] int UNIQUE,
  [amount] decimal,
  [method] nvarchar(255),
  [status] nvarchar(255),
  [created_at] datetime
)
GO

CREATE TABLE [shipping] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [order_id] int UNIQUE,
  [address] text,
  [status] nvarchar(255),
  [updated_at] datetime
)
GO

ALTER TABLE [products] ADD FOREIGN KEY ([cat_id]) REFERENCES [categories] ([cat_id])
GO

ALTER TABLE [cart] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([user_id])
GO

ALTER TABLE [cart_item] ADD FOREIGN KEY ([cart_id]) REFERENCES [cart] ([cart_id])
GO

ALTER TABLE [cart_item] ADD FOREIGN KEY ([product_id]) REFERENCES [products] ([product_id])
GO

ALTER TABLE [orders] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([user_id])
GO

ALTER TABLE [order_item] ADD FOREIGN KEY ([order_id]) REFERENCES [orders] ([order_id])
GO

ALTER TABLE [order_item] ADD FOREIGN KEY ([product_id]) REFERENCES [products] ([product_id])
GO

ALTER TABLE [payments] ADD FOREIGN KEY ([order_id]) REFERENCES [orders] ([order_id])
GO

ALTER TABLE [shipping] ADD FOREIGN KEY ([order_id]) REFERENCES [orders] ([order_id])
GO
