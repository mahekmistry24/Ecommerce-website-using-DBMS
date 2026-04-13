-- =====================================================
-- TABLE PARTITIONING for Orders
-- ADBMS: Demonstrates range partitioning by date
-- =====================================================

-- NOTE: Partitioning requires recreating the orders table.
-- This is a separate script to demonstrate the concept.
-- In production, you would create the partitioned table from the start.

-- =====================================================
-- PARTITIONED ORDERS TABLE (Alternative Design)
-- =====================================================

-- Drop existing orders cascade if switching to partitioned
-- DROP TABLE IF EXISTS orders CASCADE;

-- Create partitioned orders table
CREATE TABLE IF NOT EXISTS orders_partitioned (
    order_id SERIAL,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'pending',
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    shipping_address TEXT,
    notes TEXT,
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

-- =====================================================
-- QUARTERLY PARTITIONS FOR 2026
-- =====================================================

CREATE TABLE IF NOT EXISTS orders_2026_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE IF NOT EXISTS orders_2026_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

CREATE TABLE IF NOT EXISTS orders_2026_q3 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');

CREATE TABLE IF NOT EXISTS orders_2026_q4 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');

-- Default partition for out-of-range dates
CREATE TABLE IF NOT EXISTS orders_default PARTITION OF orders_partitioned DEFAULT;

-- =====================================================
-- INDEXES ON PARTITIONS
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_orders_part_user ON orders_partitioned(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_part_status ON orders_partitioned(status);
CREATE INDEX IF NOT EXISTS idx_orders_part_date ON orders_partitioned(order_date);

-- =====================================================
-- DEMONSTRATION QUERY
-- This query automatically targets only Q1 partition
-- =====================================================
-- EXPLAIN ANALYZE
-- SELECT * FROM orders_partitioned 
-- WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01';

-- =====================================================
-- LIST PARTITIONING EXAMPLE (for status)
-- =====================================================
CREATE TABLE IF NOT EXISTS shipments_partitioned (
    shipment_id SERIAL,
    order_id INT NOT NULL,
    warehouse_id INT,
    courier_name VARCHAR(100),
    tracking_number VARCHAR(100),
    shipment_status VARCHAR(30) NOT NULL,
    estimated_delivery DATE,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    PRIMARY KEY (shipment_id, shipment_status)
) PARTITION BY LIST (shipment_status);

CREATE TABLE IF NOT EXISTS shipments_active PARTITION OF shipments_partitioned
    FOR VALUES IN ('preparing', 'dispatched', 'in_transit', 'out_for_delivery');

CREATE TABLE IF NOT EXISTS shipments_completed PARTITION OF shipments_partitioned
    FOR VALUES IN ('delivered', 'returned');
