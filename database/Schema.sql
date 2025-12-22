CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;
CREATE TABLE suppliers(
    supplier_id INT ,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    primary key(supplier_id)
);

CREATE TABLE products (
    product_id INT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price float NOT NULL,
    stock_quantity INT DEFAULT 0,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
	primary key(product_id)

);

CREATE TABLE orders (
    order_id INT,
    product_id INT,
    quantity INT,
    order_date datetime,
    total_price float,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
	primary key(order_id)

);