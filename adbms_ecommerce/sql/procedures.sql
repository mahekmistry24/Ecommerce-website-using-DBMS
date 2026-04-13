-- =====================================================
-- PL/pgSQL Stored Procedures and Functions
-- ADBMS: Demonstrates procedural SQL capabilities
-- =====================================================

-- =====================================================
-- FUNCTION: Calculate cart total
-- Returns total amount for a given order
-- =====================================================
CREATE OR REPLACE FUNCTION calculate_cart_total(p_order_id INT)
RETURNS DECIMAL(12,2) AS $$
DECLARE
    v_total DECIMAL(12,2);
BEGIN
    SELECT COALESCE(SUM(quantity * unit_price), 0)
    INTO v_total
    FROM order_items
    WHERE order_id = p_order_id;
    
    RETURN v_total;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCTION: Get warehouse stock for a product
-- Returns total available stock across all warehouses
-- =====================================================
CREATE OR REPLACE FUNCTION get_total_stock(p_product_id VARCHAR)
RETURNS INT AS $$
DECLARE
    v_stock INT;
BEGIN
    SELECT COALESCE(SUM(quantity - reserved_quantity), 0)
    INTO v_stock
    FROM inventory
    WHERE product_id = p_product_id;
    
    RETURN v_stock;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCTION: Find best warehouse for a product
-- Returns warehouse_id with most stock
-- =====================================================
CREATE OR REPLACE FUNCTION find_best_warehouse(p_product_id VARCHAR, p_qty INT)
RETURNS INT AS $$
DECLARE
    v_warehouse_id INT;
BEGIN
    SELECT warehouse_id
    INTO v_warehouse_id
    FROM inventory i
    JOIN warehouses w ON i.warehouse_id = w.warehouse_id
    WHERE i.product_id = p_product_id
      AND (i.quantity - i.reserved_quantity) >= p_qty
      AND w.is_active = TRUE
    ORDER BY (i.quantity - i.reserved_quantity) DESC
    LIMIT 1;
    
    RETURN v_warehouse_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- PROCEDURE: Place a complete order
-- Handles order creation, inventory, payment in one transaction
-- =====================================================
CREATE OR REPLACE PROCEDURE place_order(
    p_user_id INT,
    p_shipping_address TEXT,
    p_payment_mode VARCHAR,
    p_product_ids VARCHAR[],
    p_quantities INT[],
    p_unit_prices DECIMAL[],
    p_product_names VARCHAR[],
    OUT p_order_id INT
)
LANGUAGE plpgsql AS $$
DECLARE
    v_total DECIMAL(12,2) := 0;
    v_warehouse_id INT;
    v_txn_ref VARCHAR(100);
    i INT;
BEGIN
    -- Calculate total
    FOR i IN 1..array_length(p_product_ids, 1) LOOP
        v_total := v_total + (p_quantities[i] * p_unit_prices[i]);
    END LOOP;

    -- Create order
    INSERT INTO orders (user_id, status, total_amount, shipping_address)
    VALUES (p_user_id, 'confirmed', v_total, p_shipping_address)
    RETURNING order_id INTO p_order_id;

    -- Insert order items and reduce inventory
    FOR i IN 1..array_length(p_product_ids, 1) LOOP
        -- Insert order item
        INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price)
        VALUES (p_order_id, p_product_ids[i], p_product_names[i], p_quantities[i], p_unit_prices[i]);

        -- Find best warehouse
        v_warehouse_id := find_best_warehouse(p_product_ids[i], p_quantities[i]);
        
        IF v_warehouse_id IS NOT NULL THEN
            -- Reduce inventory
            UPDATE inventory
            SET quantity = quantity - p_quantities[i],
                last_updated = CURRENT_TIMESTAMP
            WHERE product_id = p_product_ids[i]
              AND warehouse_id = v_warehouse_id;
        END IF;
    END LOOP;

    -- Create payment record
    v_txn_ref := 'TXN-' || p_order_id || '-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS');
    INSERT INTO payments (order_id, payment_mode, payment_status, amount, transaction_ref)
    VALUES (p_order_id, p_payment_mode, 'completed', v_total, v_txn_ref);

    -- Create shipment record
    IF v_warehouse_id IS NOT NULL THEN
        INSERT INTO shipments (order_id, warehouse_id, courier_name, tracking_number, shipment_status, estimated_delivery)
        VALUES (p_order_id, v_warehouse_id, 'FastShip Express', 
                'TRACK-' || p_order_id || '-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD'),
                'preparing', CURRENT_DATE + INTERVAL '5 days');
    END IF;

    RAISE NOTICE 'Order % placed successfully. Total: %', p_order_id, v_total;
END;
$$;

-- =====================================================
-- FUNCTION: Get order summary
-- Returns a formatted order summary
-- =====================================================
CREATE OR REPLACE FUNCTION get_order_summary(p_order_id INT)
RETURNS TABLE(
    item_name VARCHAR,
    qty INT,
    price DECIMAL,
    subtotal DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        oi.product_name,
        oi.quantity,
        oi.unit_price,
        (oi.quantity * oi.unit_price)::DECIMAL(10,2)
    FROM order_items oi
    WHERE oi.order_id = p_order_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- FUNCTION: Monthly revenue report
-- =====================================================
CREATE OR REPLACE FUNCTION monthly_revenue(p_year INT, p_month INT)
RETURNS DECIMAL(12,2) AS $$
DECLARE
    v_revenue DECIMAL(12,2);
BEGIN
    SELECT COALESCE(SUM(total_amount), 0)
    INTO v_revenue
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = p_year
      AND EXTRACT(MONTH FROM order_date) = p_month
      AND status != 'cancelled';
    
    RETURN v_revenue;
END;
$$ LANGUAGE plpgsql;
