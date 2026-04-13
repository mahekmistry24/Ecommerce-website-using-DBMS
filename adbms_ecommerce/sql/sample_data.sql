-- =====================================================
-- SAMPLE DATA for E-Commerce Database
-- =====================================================

-- =====================================================
-- USERS (password_hash is bcrypt hash of 'password123')
-- =====================================================
INSERT INTO users (name, email, phone, password_hash, role) VALUES
('Mahek Mistry', 'mahekmistry@gmail.com', '9876543210', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'admin'),
('Anushka Naik', 'anushkanaik@gmail.com', '9876543220', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'admin'),
('Soham Hande', 'sohamhande@gmail.com', '9876543221', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'admin'),
('Rahul Sharma', 'rahul@example.com', '9876543211', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Priya Patel', 'priya@example.com', '9876543212', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Amit Kumar', 'amit@example.com', '9876543213', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Sneha Reddy', 'sneha@example.com', '9876543214', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Vikram Singh', 'vikram@example.com', '9876543215', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Ananya Iyer', 'ananya@example.com', '9876543216', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Karan Mehta', 'karan@example.com', '9876543217', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Divya Nair', 'divya@example.com', '9876543218', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer'),
('Rohan Gupta', 'rohan@example.com', '9876543219', '$2b$12$LJ3m4ys3GZxkGJXmKvSXxeH4r1Mpv5JpFVyOfWYhqZGWKJXiVbVHK', 'customer')
ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- WAREHOUSES
-- =====================================================
INSERT INTO warehouses (warehouse_name, city, state, pincode, capacity) VALUES
('Mumbai Central Hub', 'Mumbai', 'Maharashtra', '400001', 50000),
('Delhi North Hub', 'Delhi', 'Delhi', '110001', 40000),
('Bangalore Tech Hub', 'Bangalore', 'Karnataka', '560001', 35000),
('Chennai South Hub', 'Chennai', 'Tamil Nadu', '600001', 30000),
('Kolkata East Hub', 'Kolkata', 'West Bengal', '700001', 25000)
ON CONFLICT DO NOTHING;

-- =====================================================
-- INVENTORY (distributed across warehouses)
-- =====================================================
INSERT INTO inventory (product_id, warehouse_id, quantity, reserved_quantity) VALUES
-- Electronics
('P1001', 1, 150, 10), ('P1001', 2, 120, 5), ('P1001', 3, 200, 15),
('P1002', 1, 80, 5), ('P1002', 3, 100, 8), ('P1002', 4, 60, 3),
('P1003', 2, 50, 2), ('P1003', 4, 70, 5),
('P1004', 1, 200, 20), ('P1004', 2, 180, 15), ('P1004', 5, 90, 5),
('P1005', 3, 300, 25), ('P1005', 1, 250, 20),
-- Clothing
('P2001', 1, 500, 30), ('P2001', 2, 400, 25), ('P2001', 4, 350, 20),
('P2002', 2, 200, 10), ('P2002', 3, 180, 8),
('P2003', 1, 150, 5), ('P2003', 5, 120, 3),
-- Books
('P3001', 1, 300, 15), ('P3001', 2, 250, 12), ('P3001', 3, 200, 10),
('P3002', 4, 180, 8), ('P3002', 5, 150, 5),
-- Beauty
('P4001', 1, 400, 20), ('P4001', 3, 350, 18),
('P4002', 2, 250, 12), ('P4002', 4, 200, 10)
ON CONFLICT (product_id, warehouse_id) DO NOTHING;

-- =====================================================
-- ORDERS
-- =====================================================
INSERT INTO orders (user_id, order_date, status, total_amount, shipping_address) VALUES
(2, '2026-01-15 10:30:00', 'delivered', 5498.00, '42 MG Road, Mumbai'),
(3, '2026-01-22 14:15:00', 'delivered', 2999.00, '15 Anna Nagar, Chennai'),
(4, '2026-02-05 09:00:00', 'delivered', 8497.00, '78 Koramangala, Bangalore'),
(5, '2026-02-18 16:45:00', 'shipped', 1299.00, '23 Jubilee Hills, Hyderabad'),
(2, '2026-03-01 11:20:00', 'shipped', 4998.00, '42 MG Road, Mumbai'),
(6, '2026-03-10 08:30:00', 'processing', 799.00, '56 Civil Lines, Delhi'),
(7, '2026-03-15 13:00:00', 'confirmed', 3499.00, '89 Indiranagar, Bangalore'),
(8, '2026-03-20 15:30:00', 'pending', 6997.00, '34 Park Street, Kolkata'),
(3, '2026-03-25 10:00:00', 'confirmed', 1598.00, '15 Anna Nagar, Chennai'),
(9, '2026-03-28 12:45:00', 'pending', 2499.00, '67 Baner Road, Pune'),
(4, '2026-04-01 09:15:00', 'pending', 4299.00, '78 Koramangala, Bangalore'),
(10, '2026-04-02 14:00:00', 'pending', 999.00, '12 Salt Lake, Kolkata'),
(2, '2026-04-03 16:30:00', 'confirmed', 7498.00, '42 MG Road, Mumbai'),
(5, '2026-04-04 11:00:00', 'pending', 3998.00, '23 Jubilee Hills, Hyderabad'),
(7, '2026-04-05 08:00:00', 'pending', 1799.00, '89 Indiranagar, Bangalore')
ON CONFLICT DO NOTHING;

-- =====================================================
-- ORDER ITEMS
-- =====================================================
INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price) VALUES
(1, 'P1001', 'Wireless Headphones', 1, 2499.00),
(1, 'P1002', 'Smart Watch', 1, 2999.00),
(2, 'P2001', 'Cotton T-Shirt Pack', 1, 2999.00),
(3, 'P1003', 'Bluetooth Speaker', 2, 1799.00),
(3, 'P1001', 'Wireless Headphones', 1, 2499.00),
(3, 'P3001', 'Database Systems Book', 1, 2400.00),
(4, 'P2002', 'Denim Jeans', 1, 1299.00),
(5, 'P1001', 'Wireless Headphones', 2, 2499.00),
(6, 'P3002', 'Python Programming Book', 1, 799.00),
(7, 'P1004', 'USB-C Hub', 1, 3499.00),
(8, 'P1002', 'Smart Watch', 1, 2999.00),
(8, 'P4001', 'Face Serum Set', 2, 1999.00),
(9, 'P2003', 'Running Shoes', 1, 1598.00),
(10, 'P1001', 'Wireless Headphones', 1, 2499.00),
(11, 'P1005', 'Laptop Stand', 1, 4299.00),
(12, 'P4002', 'Hair Care Kit', 1, 999.00),
(13, 'P1002', 'Smart Watch', 1, 2999.00),
(13, 'P1001', 'Wireless Headphones', 1, 2499.00),
(13, 'P3001', 'Database Systems Book', 1, 2400.00),
(14, 'P4001', 'Face Serum Set', 2, 1999.00),
(15, 'P2002', 'Denim Jeans', 1, 1299.00),
(15, 'P3002', 'Python Programming Book', 1, 799.00)
ON CONFLICT DO NOTHING;

-- =====================================================
-- PAYMENTS
-- =====================================================
INSERT INTO payments (order_id, payment_mode, payment_status, amount, transaction_ref) VALUES
(1, 'upi', 'completed', 5498.00, 'TXN-1-20260115103000'),
(2, 'credit_card', 'completed', 2999.00, 'TXN-2-20260122141500'),
(3, 'debit_card', 'completed', 8497.00, 'TXN-3-20260205090000'),
(4, 'upi', 'completed', 1299.00, 'TXN-4-20260218164500'),
(5, 'net_banking', 'completed', 4998.00, 'TXN-5-20260301112000'),
(6, 'wallet', 'completed', 799.00, 'TXN-6-20260310083000'),
(7, 'credit_card', 'completed', 3499.00, 'TXN-7-20260315130000'),
(8, 'cod', 'pending', 6997.00, 'TXN-8-20260320153000'),
(9, 'upi', 'completed', 1598.00, 'TXN-9-20260325100000'),
(10, 'debit_card', 'pending', 2499.00, 'TXN-10-20260328124500'),
(11, 'upi', 'pending', 4299.00, 'TXN-11-20260401091500'),
(12, 'wallet', 'pending', 999.00, 'TXN-12-20260402140000'),
(13, 'credit_card', 'completed', 7498.00, 'TXN-13-20260403163000'),
(14, 'upi', 'pending', 3998.00, 'TXN-14-20260404110000'),
(15, 'cod', 'pending', 1799.00, 'TXN-15-20260405080000')
ON CONFLICT DO NOTHING;

-- =====================================================
-- SHIPMENTS
-- =====================================================
INSERT INTO shipments (order_id, warehouse_id, courier_name, tracking_number, shipment_status, estimated_delivery, shipped_at, delivered_at) VALUES
(1, 1, 'BlueDart', 'TRACK-1-20260115', 'delivered', '2026-01-20', '2026-01-16 08:00:00', '2026-01-19 14:30:00'),
(2, 4, 'DTDC', 'TRACK-2-20260122', 'delivered', '2026-01-27', '2026-01-23 09:00:00', '2026-01-26 11:00:00'),
(3, 3, 'Delhivery', 'TRACK-3-20260205', 'delivered', '2026-02-10', '2026-02-06 10:00:00', '2026-02-09 15:00:00'),
(4, 1, 'BlueDart', 'TRACK-4-20260218', 'in_transit', '2026-02-23', '2026-02-19 08:00:00', NULL),
(5, 1, 'Delhivery', 'TRACK-5-20260301', 'dispatched', '2026-03-06', '2026-03-02 10:00:00', NULL),
(6, 2, 'DTDC', 'TRACK-6-20260310', 'preparing', '2026-03-15', NULL, NULL),
(7, 3, 'BlueDart', 'TRACK-7-20260315', 'preparing', '2026-03-20', NULL, NULL),
(8, 5, 'Delhivery', 'TRACK-8-20260320', 'preparing', '2026-03-25', NULL, NULL)
ON CONFLICT DO NOTHING;
