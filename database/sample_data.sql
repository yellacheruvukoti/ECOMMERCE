-----------------------------------------
-- USERS TABLE
-----------------------------------------
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    phone VARCHAR(20),
    created_at DATETIME DEFAULT GETDATE()
);

INSERT INTO users (name, email, password, phone)
VALUES
('Ravi Kumar', 'ravi@example.com', '1234', '9876543210'),
('Sita Devi', 'sita@example.com', '1234', '9998887776');


-----------------------------------------
-- ADDRESSES TABLE
-----------------------------------------
CREATE TABLE addresses (
    address_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    full_name VARCHAR(100),
    address_line VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    phone VARCHAR(20)
);

INSERT INTO addresses (user_id, full_name, address_line, city, state, pincode, phone)
VALUES
(1, 'Ravi Kumar', '12 MG Road', 'Bengaluru', 'Karnataka', '560001', '9876543210'),
(2, 'Sita Devi', '45 LB Nagar', 'Hyderabad', 'Telangana', '500074', '9998887776');


-----------------------------------------
-- CATEGORIES TABLE
-----------------------------------------
CREATE TABLE categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO categories (name) VALUES
('Electronics'),
('Mobiles'),
('Fashion'),
('Accessories');


-----------------------------------------
-- PRODUCTS TABLE
-----------------------------------------
CREATE TABLE products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    category_id INT FOREIGN KEY REFERENCES categories(category_id),
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    discount_price DECIMAL(10,2),
    stock INT
);

INSERT INTO products (category_id, name, description, price, discount_price, stock)
VALUES
(1, 'HP Laptop 15s', 'i5 12th Gen, 8GB RAM, 512GB SSD', 60000, 55000, 10),
(2, 'iPhone 14', '128GB, A15 Bionic', 80000, 76000, 15),
(3, 'Men T-Shirt', 'Cotton, Regular Fit', 600, 450, 50),
(4, 'Fast Charger', '25W Super Fast Charging', 1500, 999, 40);


-----------------------------------------
-- PRODUCT IMAGES
-----------------------------------------
CREATE TABLE product_images (
    image_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT FOREIGN KEY REFERENCES products(product_id),
    image_url VARCHAR(255)
);

INSERT INTO product_images (product_id, image_url)
VALUES
(1, 'https://example.com/laptop1.jpg'),
(2, 'https://example.com/iphone1.jpg'),
(3, 'https://example.com/tshirt1.jpg'),
(4, 'https://example.com/charger1.jpg');


-----------------------------------------
-- CART TABLE
-----------------------------------------
CREATE TABLE cart (
    cart_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id)
);

INSERT INTO cart (user_id) VALUES
(1), (2);


-----------------------------------------
-- CART ITEMS
-----------------------------------------
CREATE TABLE cart_items (
    cart_item_id INT IDENTITY(1,1) PRIMARY KEY,
    cart_id INT FOREIGN KEY REFERENCES cart(cart_id),
    product_id INT FOREIGN KEY REFERENCES products(product_id),
    quantity INT
);

INSERT INTO cart_items (cart_id, product_id, quantity)
VALUES
(1, 1, 1),
(1, 4, 2),
(2, 3, 1);


-----------------------------------------
-- ORDERS TABLE
-----------------------------------------
CREATE TABLE orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    address_id INT FOREIGN KEY REFERENCES addresses(address_id),
    total_amount DECIMAL(10,2),
    status VARCHAR(50),
    created_at DATETIME DEFAULT GETDATE()
);

INSERT INTO orders (user_id, address_id, total_amount, status)
VALUES
(1, 1, 56000, 'Processing');


-----------------------------------------
-- ORDER ITEMS TABLE
-----------------------------------------
CREATE TABLE order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT FOREIGN KEY REFERENCES orders(order_id),
    product_id INT FOREIGN KEY REFERENCES products(product_id),
    quantity INT,
    price_at_purchase DECIMAL(10,2)
);

INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
VALUES
(1, 1, 1, 55000),
(1, 4, 1, 999);
