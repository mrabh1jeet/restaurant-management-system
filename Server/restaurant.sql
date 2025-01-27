-- Use the restaurant database
USE restaurant;

-- alembic_version: stores version information for migrations
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) PRIMARY KEY
);

-- customer: stores customer details
CREATE TABLE IF NOT EXISTS customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(255) NOT NULL,
    cust_mail VARCHAR(255) NOT NULL,
    cust_phone VARCHAR(20) NOT NULL
);

-- customer_log: stores logs related to customer activities
CREATE TABLE IF NOT EXISTS customer_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    action VARCHAR(255) NOT NULL,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);

-- feedback: stores customer feedback
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT
);

-- items: stores item details, separate from menu items if they are generic
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- menu_item: specific items listed on the menu
CREATE TABLE IF NOT EXISTS menu_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- order: stores order details
CREATE TABLE IF NOT EXISTS `order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE SET NULL
);

-- order_item: stores items within each order
CREATE TABLE IF NOT EXISTS order_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menu_item_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id) ON DELETE SET NULL
);

-- order_totals: tracks order totals
CREATE TABLE IF NOT EXISTS order_totals (
    order_id INT PRIMARY KEY,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(id) ON DELETE CASCADE
);

-- reservation: stores reservations for tables
CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    table_id INT,
    reservation_time DATETIME NOT NULL,
    FOREIGN KEY (table_id) REFERENCES `table`(id) ON DELETE SET NULL
);

-- staff: stores staff information
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    position VARCHAR(255) NOT NULL
);

-- table: stores table information in the restaurant
CREATE TABLE IF NOT EXISTS `table` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_people INT NOT NULL,
    is_reserved BOOLEAN DEFAULT FALSE
);

-- users: stores user login information
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Insert sample data into menu_item
-- INSERT INTO menu_item (name, description, price) VALUES 
-- ('Pasta', 'Delicious pasta with marinara sauce', 12.99),
-- ('Burger', 'Juicy beef burger with cheese and lettuce', 10.99),
-- ('Salad', 'Fresh mixed greens with vinaigrette', 8.99);

-- -- Insert sample data into staff
-- INSERT INTO staff (name, phone, position) VALUES 
-- ('Alice Johnson', '555-0100', 'Waiter'),
-- ('Bob Smith', '555-0200', 'Chef'),
-- ('Carol Adams', '555-0300', 'Manager');
