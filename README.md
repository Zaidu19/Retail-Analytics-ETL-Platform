# 🛍️ Retail Analytics & ETL Platform

A production-style Retail Analytics Platform built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** that simulates a real-world e-commerce backend.

The platform manages customers, products, orders, payments, refunds, inventory, and business analytics while implementing secure authentication, Role-Based Access Control (RBAC), and reporting APIs.

---

# 🚀 Features

## Authentication & Authorization

- JWT Authentication
- Password Hashing
- Role-Based Access Control (RBAC)
- Secure Login
- User Registration
- Admin Role Management

Roles:

- Customer
- Business Analyst
- Admin
- Inventory Manager

---

## Customer Management

- Create Customer Profile
- View Own Profile (`/customers/me`)
- Update Own Profile
- Admin Customer Management
- Customer Order History

---

## Product & Category Management

- Product CRUD
- Category CRUD
- Inventory Tracking
- Low Stock Monitoring
- Product Relationships

---

## Order Management

- Create Orders
- Automatic Order Items
- Automatic Stock Reduction
- Order Status Workflow

```
Pending
        ↓
Paid
        ↓
Shipped
        ↓
Delivered
        ↓
Completed
```

- Cancel Orders
- Restore Inventory on Cancellation

---

## Payment Module

- Cash Payments
- Online Payments
- Payment Status Workflow
- Automatic Order Status Updates

---

## Refund Workflow

- Request Refund
- Approve Refund
- Reject Refund
- Automatic Payment Refund
- Inventory Restoration
- Refund Status Tracking

---

## Inventory Logs

Automatic inventory logs for:

- Sales
- Restocks
- Returns
- Damage
- Manual Adjustments

---

## Analytics APIs

### Dashboard

- Total Customers
- Total Products
- Total Orders
- Completed Orders
- Refunded Orders
- Revenue
- Refund Amount
- Low Stock Count

### Sales Analytics

- Monthly Sales
- Top Products
- Top Customers
- Category Sales

### Refund Analytics

- Refund Count
- Refund Amount
- Refund Rate

### Inventory Analytics

- Low Stock Products
- Out of Stock Products
- Inventory Value
- Inventory Movements

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python 3.13
- SQLAlchemy 2.0
- Alembic
- Pydantic v2

## Database

- PostgreSQL

## Authentication

- JWT
- Passlib (bcrypt)

## Analytics

- SQL Aggregations
- Group By
- Joins
- Window-ready Queries

## Testing

- Pytest
- TestClient

## Data

- Pandas

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```
src/
│
├── analytics/
├── auth/
├── categories/
├── customers/
├── inventory_logs/
├── orderitems/
├── orders/
├── payments/
├── products/
├── refunds/
├── users/
│
├── common/
├── db/
├── utils/
└── main.py
```

---

# 🗄 Database Schema
The following Entity Relationship Diagram (ERD) represents the database design of the Retail Analytics & ETL Platform.

![ER Diagram](images/er-diagram.png)
---

# 🔐 RBAC

| Module           | Customer |     Inventory Manager     | Business Analyst |   Admin  |
| ---------------- | :------: | :-----------------------: | :--------------: | :------: |
| Register/Login   |     ✅    |             ✅             |         ✅        |     ✅    |
| Customer Profile |    Own   |             ❌             |       Read       |   Full   |
| Products         |   Read   |        Update Stock       |       Read       |   CRUD   |
| Categories       |   Read   |            Read           |       Read       |   CRUD   |
| Orders           |    Own   |            Read           |       Read       |   Full   |
| Payments         |    Own   |            Read           |       Read       |   Full   |
| Refunds          |    Own   |      Process Returns      |       Read       |   Full   |
| Inventory Logs   |     ❌    |            CRUD           |       Read       |   Full   |
| Analytics        |     ❌    | Inventory Only (optional) |     Read All     | Read All |
| User Roles       |     ❌    |             ❌             |         ❌        |  Manage  |

---

# 📊 Analytics

Implemented business reports include:

- Dashboard KPIs
- Monthly Revenue
- Top Selling Products
- Top Customers
- Category Sales
- Refund Analytics
- Inventory Analytics

---

# ⚙️ Installation

```bash
git clone https://github.com/yourusername/Retail-Analytics-ETL-Platform.git

cd Retail-Analytics-ETL-Platform
```

Create virtual environment

```bash
python -m venv env
```

Activate

Windows

```bash
env\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
alembic upgrade head
```

Run server

```bash
uvicorn src.main:app --reload
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🧪 Testing

Run tests

```bash
pytest
```

---

# 📸 Screenshots

Add screenshots here:

- Swagger UI
- Analytics Dashboard
- PostgreSQL Tables
- Power BI Dashboard (Coming Soon)

---

# 🚀 Future Improvements

- Docker Containerization
- AWS Deployment
- CI/CD with GitHub Actions
- MongoDB Activity Logs
- Redis Caching
- Email Notifications
- Power BI Dashboards
- Faker Data Generation
- Advanced ETL Pipelines

---

# 👨‍💻 Author

**Mohammad Zaid Ansari**

B.Tech CSE

Python Backend Developer | Data Analytics Enthusiast