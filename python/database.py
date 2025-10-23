import mysql.connector

# Connexion au serveur MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="xxxxxxxxxxx",
    password="xxxxxxxxxxxxx"
)
cursor = conn.cursor()

# Création de la base de données
cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_analytics;")
print("Base de données 'restaurant_analytics' créée avec succès.")

# Use de le base
cursor.execute("USE restaurant_analytics;")

# Création des tables 
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(100),
    region VARCHAR(100),
    registration_date DATE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    menu_id INT AUTO_INCREMENT PRIMARY KEY,
    dish_name VARCHAR(100),
    price DECIMAL(10,2)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(12,2)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    menu_id INT,
    staff_id INT,
    order_date DATE,
    quantity INT,
    total_amount DECIMAL(12,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_person VARCHAR(100),
    delivery_time DATETIME,
    status VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    staff_id INT,
    booking_date DATE,
    num_people INT,
    status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);
""")

print("Tables ont été créées avec succès.")

cursor.close()
conn.close()
