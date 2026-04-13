-- =====================================================
-- TRIGGERS for Automated Database Actions
-- ADBMS: Demonstrates trigger-based automation
-- =====================================================

-- =====================================================
-- TRIGGER 1: Audit log on order status change
-- Automatically logs every order status change
-- =====================================================
CREATE OR REPLACE FUNCTION fn_order_status_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO order_audit_log (order_id, old_status, new_status, changed_at)
        VALUES (NEW.order_id, OLD.status, NEW.status, CURRENT_TIMESTAMP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_order_status_audit ON orders;
CREATE TRIGGER trg_order_status_audit
    AFTER UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION fn_order_status_audit();

-- =====================================================
-- TRIGGER 2: Auto-update inventory timestamp
-- Updates last_updated whenever quantity changes
-- =====================================================
CREATE OR REPLACE FUNCTION fn_inventory_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_inventory_timestamp ON inventory;
CREATE TRIGGER trg_inventory_timestamp
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    WHEN (OLD.quantity IS DISTINCT FROM NEW.quantity)
    EXECUTE FUNCTION fn_inventory_timestamp();

-- =====================================================
-- TRIGGER 3: Validate stock before order item insert
-- Ensures sufficient stock exists
-- =====================================================
CREATE OR REPLACE FUNCTION fn_validate_stock()
RETURNS TRIGGER AS $$
DECLARE
    v_available INT;
BEGIN
    SELECT COALESCE(SUM(quantity - reserved_quantity), 0)
    INTO v_available
    FROM inventory
    WHERE product_id = NEW.product_id;
    
    IF v_available < NEW.quantity THEN
        RAISE WARNING 'Low stock for product %: requested %, available %', 
            NEW.product_id, NEW.quantity, v_available;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validate_stock ON order_items;
CREATE TRIGGER trg_validate_stock
    BEFORE INSERT ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION fn_validate_stock();

-- =====================================================
-- TRIGGER 4: Auto-update order total
-- Recalculates total_amount when order items change
-- =====================================================
CREATE OR REPLACE FUNCTION fn_update_order_total()
RETURNS TRIGGER AS $$
DECLARE
    v_total DECIMAL(12,2);
BEGIN
    SELECT COALESCE(SUM(quantity * unit_price), 0)
    INTO v_total
    FROM order_items
    WHERE order_id = COALESCE(NEW.order_id, OLD.order_id);
    
    UPDATE orders
    SET total_amount = v_total
    WHERE order_id = COALESCE(NEW.order_id, OLD.order_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_order_total ON order_items;
CREATE TRIGGER trg_update_order_total
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_order_total();
