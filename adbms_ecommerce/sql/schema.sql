-- =====================================================
-- Smart Distributed E-Commerce Database System
-- PostgreSQL Schema - ADBMS Project
-- =====================================================

-- Create database (run separately if needed)
-- CREATE DATABASE adbms_ecommerce;

-- =====================================================
-- TABLE 1: users
-- Stores customer/admin details
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'customer' CHECK (role IN ('customer', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE 2: warehouses
-- Stores warehouse/distribution center locations
-- =====================================================
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(10),
    capacity INT DEFAULT 10000,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE 3: inventory
-- Distributed stock across warehouses
-- =====================================================
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    warehouse_id INT REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reserved_quantity INT DEFAULT 0 CHECK (reserved_quantity >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, warehouse_id)
);

-- =====================================================
-- TABLE 4: orders
-- Purchase orders from customers
-- =====================================================
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    shipping_address TEXT,
    notes TEXT
);

-- =====================================================
-- TABLE 5: order_items
-- Individual products within each order
-- =====================================================
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL
);

-- =====================================================
-- TABLE 6: payments
-- Payment records for orders
-- =====================================================
CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    payment_mode VARCHAR(30) NOT NULL CHECK (payment_mode IN ('credit_card', 'debit_card', 'upi', 'net_banking', 'cod', 'wallet')),
    payment_status VARCHAR(30) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    amount DECIMAL(12,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_ref VARCHAR(100)
);

-- =====================================================
-- TABLE 7: shipments
-- Delivery tracking for orders
-- =====================================================
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    warehouse_id INT REFERENCES warehouses(warehouse_id),
    courier_name VARCHAR(100),
    tracking_number VARCHAR(100),
    shipment_status VARCHAR(30) DEFAULT 'preparing' CHECK (shipment_status IN ('preparing', 'dispatched', 'in_transit', 'out_for_delivery', 'delivered', 'returned')),
    estimated_delivery DATE,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- =====================================================
-- TABLE 8: order_audit_log
-- Audit trail for order status changes (used by trigger)
-- =====================================================
CREATE TABLE IF NOT EXISTS order_audit_log (
    log_id SERIAL PRIMARY KEY,
    order_id INT,
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100) DEFAULT 'system'
);
