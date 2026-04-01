-- schema.sql
-- MySQL database schema for Estate X – Online Property Selling System
-- Run this file in your MySQL client to set up the database

CREATE DATABASE IF NOT EXISTS estate_x;
USE estate_x;

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- stored as hashed value
    phone VARCHAR(20),
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: properties
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    description TEXT,
    bedrooms INT DEFAULT 0,
    bathrooms INT DEFAULT 0,
    area DECIMAL(10, 2) DEFAULT 0,         -- area in sq ft
    image_path VARCHAR(300),               -- relative path to uploaded image
    status ENUM('Available', 'Sold') DEFAULT 'Available',
    is_verified TINYINT(1) DEFAULT 0,      -- 0 = Not Verified, 1 = Verified
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    booking_date DATE NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    payment_status ENUM('Pending', 'Paid') DEFAULT 'Pending',
    agreement_number VARCHAR(50) UNIQUE,    -- system-generated unique agreement number
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Table: wishlist
CREATE TABLE IF NOT EXISTS wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_wishlist (user_id, property_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Insert a default admin user (password: admin123)
-- Run this after setting up the tables
-- Password below is for 'admin123' hashed with werkzeug pbkdf2:sha256
INSERT INTO users (name, email, password, phone, role)
VALUES (
    'Admin',
    'admin@estatex.com',
    'pbkdf2:sha256:260000$placeholder',  -- Will be replaced at runtime
    '9999999999',
    'admin'
)
ON DUPLICATE KEY UPDATE name=name;
