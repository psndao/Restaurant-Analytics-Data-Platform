/********************************************************************************************
   PROJET : Restaurant Analytics Data Platform
   AUTEUR : Pape Semou NDAO
   DATE  : 2025-10-24
   DESCRIPTION :
        Schéma complet pour la base MySQL "restaurant_analytics", incluant :
        - la création des tables de gestion du restaurant (clients, commandes, menu, etc.)
        - la définition des relations et clés étrangères
        - la création de vues analytiques pour le reporting
********************************************************************************************/

-- Nettoyage préalable
DROP DATABASE IF EXISTS restaurant_analytics;
CREATE DATABASE restaurant_analytics;
USE restaurant_analytics;

/********************************************************************************************
   TABLE CLIENTS — customers
********************************************************************************************/
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique du client',
    name VARCHAR(100) COMMENT 'Nom du client',
    email VARCHAR(150) COMMENT 'Adresse e-mail du client',
    phone VARCHAR(50) COMMENT 'Numéro de téléphone',
    city VARCHAR(100) COMMENT 'Ville du client',
    region VARCHAR(100) COMMENT 'Région du client',
    registration_date DATE COMMENT 'Date d’enregistrement du client'
);

/********************************************************************************************
   TABLE PERSONNEL — staff
********************************************************************************************/
CREATE TABLE staff (
    staff_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique du personnel',
    name VARCHAR(100) COMMENT 'Nom du membre du personnel',
    role VARCHAR(50) COMMENT 'Rôle (Serveur, Cuisinier, Livreuse...)',
    hire_date DATE COMMENT 'Date d’embauche',
    salary DECIMAL(12,2) COMMENT 'Salaire brut'
);

/********************************************************************************************
   TABLE MENU — menu
********************************************************************************************/
CREATE TABLE menu (
    menu_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique du plat',
    dish_name VARCHAR(100) COMMENT 'Nom du plat',
    price DECIMAL(10,2) COMMENT 'Prix du plat en FCFA'
);

/********************************************************************************************
   TABLE COMMANDES — orders
********************************************************************************************/
CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique de la commande',
    customer_id VARCHAR(10) COMMENT 'Client ayant passé la commande',
    menu_id VARCHAR(10) COMMENT 'Plat commandé',
    staff_id VARCHAR(10) COMMENT 'Personnel ayant pris la commande',
    order_date DATE COMMENT 'Date de la commande',
    quantity INT COMMENT 'Quantité commandée',
    total_amount DECIMAL(10,2) COMMENT 'Montant total de la commande',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

/********************************************************************************************
   TABLE LIVRAISONS — deliveries
********************************************************************************************/
CREATE TABLE deliveries (
    delivery_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique de la livraison',
    order_id VARCHAR(10) COMMENT 'Commande associée',
    delivery_person VARCHAR(100) COMMENT 'Nom du livreur',
    delivery_time DATETIME COMMENT 'Date et heure de la livraison',
    status VARCHAR(50) COMMENT 'Statut de la livraison (Livré, En cours, Annulé)',
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

/********************************************************************************************
   TABLE RÉSERVATIONS — bookings
********************************************************************************************/
CREATE TABLE bookings (
    booking_id VARCHAR(10) PRIMARY KEY COMMENT 'Identifiant unique de la réservation',
    customer_id VARCHAR(10) COMMENT 'Client ayant réservé',
    staff_id VARCHAR(10) COMMENT 'Personnel en charge',
    booking_date DATE COMMENT 'Date de la réservation',
    num_people INT COMMENT 'Nombre de personnes',
    status VARCHAR(50) COMMENT 'Statut (Confirmée, Annulée)',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

/********************************************************************************************
   VUES ANALYTIQUES — pour reporting et BI
********************************************************************************************/

-- 7.1. Chiffre d’affaires par plat
CREATE OR REPLACE VIEW v_sales_by_menu AS
SELECT 
    m.dish_name,
    SUM(o.quantity) AS total_quantity,
    SUM(o.total_amount) AS total_revenue
FROM orders o
JOIN menu m ON o.menu_id = m.menu_id
GROUP BY m.dish_name
ORDER BY total_revenue DESC;

-- 7.2. Performance du personnel
CREATE OR REPLACE VIEW v_staff_performance AS
SELECT 
    s.name AS staff_name,
    s.role,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_sales
FROM staff s
LEFT JOIN orders o ON s.staff_id = o.staff_id
GROUP BY s.staff_id
ORDER BY total_sales DESC;

-- 7.3. Répartition des statuts de livraison
CREATE OR REPLACE VIEW v_delivery_status AS
SELECT 
    status,
    COUNT(*) AS total_deliveries,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM deliveries), 1) AS pct
FROM deliveries
GROUP BY status;

-- 7.4. Réservations par mois
CREATE OR REPLACE VIEW v_bookings_monthly AS
SELECT 
    DATE_FORMAT(booking_date, '%Y-%m') AS month,
    COUNT(*) AS total_bookings,
    SUM(num_people) AS total_guests
FROM bookings
GROUP BY month
ORDER BY month;

/********************************************************************************************
   TESTS RAPIDES
********************************************************************************************/
USE restaurant_analytics;

-- Vérification du chargement des données
SELECT COUNT(*) AS nb_orders FROM orders;
SELECT * FROM bookings LIMIT 5;
