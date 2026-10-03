CREATE DATABASE IF NOT EXISTS ewaste_locator;
USE ewaste_locator;

CREATE TABLE IF NOT EXISTS facilities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10),
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    contact VARCHAR(30),
    email VARCHAR(150),
    operating_hours VARCHAR(150),
    accepted_categories VARCHAR(255) NOT NULL,
    verification_status ENUM('Verified','Pending','Expired') NOT NULL DEFAULT 'Pending',
    verification_source VARCHAR(255),
    last_verified DATE,
    website VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_city (city),
    INDEX idx_status (verification_status),
    INDEX idx_lat_lng (latitude, longitude)
);
