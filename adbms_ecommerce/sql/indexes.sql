-- =====================================================
-- INDEXES for Query Optimization
-- ADBMS: Demonstrates index-based performance improvement
-- =====================================================

-- User lookups by email (login)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Order lookups by user (order history)
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);

-- Order filtering by status
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- Order date range queries
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date DESC);

-- Inventory lookups by product (stock check)
CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);

-- Inventory lookups by warehouse
CREATE INDEX IF NOT EXISTS idx_inventory_warehouse_id ON inventory(warehouse_id);

-- Composite index: find product stock in specific warehouse
CREATE INDEX IF NOT EXISTS idx_inventory_product_warehouse ON inventory(product_id, warehouse_id);

-- Order items by order (order details)
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- Payments by order
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);

-- Shipments by order
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);

-- Audit log by order
CREATE INDEX IF NOT EXISTS idx_audit_order_id ON order_audit_log(order_id);

-- =====================================================
-- QUERY OPTIMIZATION DEMONSTRATION
-- Run these to compare performance before/after indexes
-- =====================================================

-- Example: EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1;
-- Example: EXPLAIN ANALYZE SELECT * FROM inventory WHERE product_id = 'P1001';
-- Example: EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01';
