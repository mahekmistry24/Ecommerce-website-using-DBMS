# 🛒 Smart Distributed E-Commerce Database System

**Advanced Database Management System (ADBMS) Project**

A full-stack e-commerce backend system demonstrating hybrid relational (PostgreSQL) + NoSQL (MongoDB) database architecture with distributed inventory management, query optimization, and XML support.

---

## 🎯 Project Overview

This project simulates a real-world e-commerce platform where:
- Users register, browse products, and place orders
- Products are stored in a flexible NoSQL catalog (MongoDB)
- Orders, payments, and shipments use ACID transactions (PostgreSQL)
- Inventory is distributed across 5 warehouses
- Reviews and activity logs use document-style storage
- Queries are optimized with indexes and analyzed with EXPLAIN ANALYZE

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              STREAMLIT FRONTEND              │
│   Home │ Products │ Cart │ Orders │ Admin    │
└──────────────────┬──────────────────────────┘
                   │ REST API
┌──────────────────┴──────────────────────────┐
│              FASTAPI BACKEND                 │
│   Auth │ Products │ Orders │ Inventory       │
│   Reviews │ Analytics │ XML                  │
└──────┬───────────────────────┬──────────────┘
       │                       │
┌──────┴──────┐       ┌───────┴───────┐
│ PostgreSQL  │       │   MongoDB     │
│ (Relational)│       │   (NoSQL)     │
│             │       │               │
│ • Users     │       │ • Products    │
│ • Orders    │       │ • Reviews     │
│ • Payments  │       │ • Logs        │
│ • Inventory │       │               │
│ • Shipments │       │               │
│ • Warehouses│       │               │
└─────────────┘       └───────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Python + FastAPI | REST API server |
| Relational DB | PostgreSQL 18 | Transactional data |
| NoSQL DB | MongoDB 8.2 | Document/catalog data |
| ORM | SQLAlchemy 2.0 | PostgreSQL ORM |
| Frontend | Streamlit | Interactive dashboard |
| Auth | JWT + bcrypt | Authentication |
| XML | lxml | XML import/export |
| Charts | Plotly | Data visualization |

---

## 📚 ADBMS Topics Covered

| Topic | Implementation |
|-------|---------------|
| **EER & Data Modeling** | 8 PostgreSQL tables with relationships |
| **Distributed Databases** | Inventory across 5 warehouses |
| **NoSQL / MongoDB** | Products, reviews, logs collections |
| **Query Optimization** | EXPLAIN ANALYZE + strategic indexes |
| **PL/SQL** | Stored procedures, functions, triggers |
| **Table Partitioning** | Range partitioning on orders by quarter |
| **XML / Semi-structured** | Order XML export, product XML import |
| **Transactions** | ACID-compliant order placement |
| **Aggregation** | MongoDB pipelines for analytics |
| **Indexing** | B-tree, composite, and text indexes |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- PostgreSQL 15+
- MongoDB 6+

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure environment
Edit `backend/.env` with your database credentials.

### 3. Start the backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
The database tables and sample data will be created automatically on startup.

### 4. Start the frontend
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### 5. Access
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501

---

## 📁 Project Structure

```
adbms_ecommerce/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── config.py        # Configuration
│   │   ├── db/              # Database connections
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helpers (auth, XML, logging)
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app.py               # Streamlit main app
│   └── pages/               # Streamlit pages
├── sql/                     # PostgreSQL scripts
├── mongodb/                 # MongoDB sample data
├── xml/                     # XML samples
└── docs/                    # Documentation
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login |
| GET | `/api/products` | List products |
| GET | `/api/products/search?q=...` | Search products |
| POST | `/api/orders` | Place order |
| GET | `/api/orders/user/{id}` | Order history |
| GET | `/api/inventory/product/{id}` | Stock check |
| POST | `/api/reviews` | Add review |
| GET | `/api/analytics/top-products` | Top products |
| GET | `/api/xml/order/{id}` | XML export |

---

## 👤 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | mahekmistry@gmail.com | password123 |
| User | rahul@example.com | password123 |
| User | priya@example.com | password123 |

---

## 📝 License

This project is for academic purposes — ADBMS Course Project 2026.
