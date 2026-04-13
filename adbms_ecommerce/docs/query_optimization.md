# Query Optimization Analysis

## Smart Distributed E-Commerce System

### 1. Index Strategy

#### PostgreSQL Indexes
| Table | Column(s) | Index Type | Purpose |
|-------|-----------|-----------|---------|
| users | email | B-tree (Unique) | Login lookup |
| orders | user_id | B-tree | Order history |
| orders | status | B-tree | Status filtering |
| orders | order_date | B-tree DESC | Date range queries |
| inventory | product_id | B-tree | Stock lookup |
| inventory | (product_id, warehouse_id) | Composite | Product-warehouse lookup |
| order_items | order_id | B-tree | Order details |
| payments | order_id | B-tree | Payment lookup |

#### MongoDB Indexes
| Collection | Field(s) | Index Type | Purpose |
|-----------|----------|-----------|---------|
| products | product_id | Unique | Product lookup |
| products | category | Single | Category filter |
| products | brand | Single | Brand filter |
| products | price | Single | Price range |
| products | name, brand, category | Text | Full-text search |
| reviews | product_id | Single | Product reviews |
| logs | user_id | Single | User activity |
| logs | event_type | Single | Event filtering |

### 2. Query Performance Examples

Run these in the Analytics → Query Performance tab to see EXPLAIN ANALYZE results.

#### Without Index (Sequential Scan)
```sql
-- Before creating index on orders.user_id
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2;
-- Result: Seq Scan on orders, cost ~1.00..1.20
```

#### With Index (Index Scan)
```sql
-- After creating index on orders.user_id
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2;
-- Result: Index Scan using idx_orders_user_id, cost ~0.15..8.17
```

### 3. Partitioning Benefits

The orders table is partitioned by quarter:
- orders_2026_q1: Jan-Mar 2026
- orders_2026_q2: Apr-Jun 2026
- orders_2026_q3: Jul-Sep 2026
- orders_2026_q4: Oct-Dec 2026

```sql
-- This query only scans Q1 partition
EXPLAIN ANALYZE
SELECT * FROM orders_partitioned
WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01';
-- Result: Scans only orders_2026_q1, skips other partitions
```

### 4. MongoDB Aggregation Performance

MongoDB aggregation pipelines with indexes:

```javascript
// Category statistics - uses category index
db.products.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 }, avg_price: { $avg: "$price" } } }
]);

// Top-rated products - uses ratings_summary index
db.products.aggregate([
  { $match: { "ratings_summary.review_count": { $gte: 5 } } },
  { $sort: { "ratings_summary.avg_rating": -1 } },
  { $limit: 10 }
]);
```

### 5. Transaction Consistency

Order placement uses PostgreSQL transactions to ensure:
- **Atomicity**: All or nothing (order + items + payment + shipment)
- **Consistency**: Inventory constraints maintained
- **Isolation**: Concurrent orders don't conflict
- **Durability**: Committed data persists

```python
# Simplified transaction flow
db.begin()
try:
    order = create_order()
    items = create_order_items()
    reduce_inventory()
    create_payment()
    create_shipment()
    db.commit()  # All succeed
except:
    db.rollback()  # All fail
```
