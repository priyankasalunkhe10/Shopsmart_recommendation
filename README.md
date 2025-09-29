# 🛍️ ShopSmart – Location-Based Product Recommendation System

ShopSmart is a Flask-based web application that provides **location-based product recommendations** to customers.  
It analyzes transactions of customers in the same location to suggest the most popular products, helping businesses improve sales and engagement.

---

## 🚀 Features
- 🔑 **Customer Login** – Authenticate customers using their ID.  
- 📍 **Location-Based Recommendations** – Suggests products purchased by customers in the same location.  
- 📦 **Product & Transaction Management** – Manage products and purchases through APIs.  
- 📂 **CSV Importer** – Load customers, products, and transactions directly from CSV files into MySQL.  
- 🔗 **RESTful APIs** – For customers, products, and transactions.  
- 🧪 **Postman Tested** – All endpoints verified for reliability.  

---

## 🛠️ Tech Stack
- **Backend:** Flask, Python  
- **Database:** MySQL, SQLAlchemy ORM  
- **Data Processing:** Pandas  
- **API Testing:** Postman  
- **Version Control:** Git, GitHub  

---

## 📂 Project Structure
```
Shopsmart_recommendation/
│── main.py 
│── database.py
│── csv_importer.py 
│── recommender_utils.py 
│── models/
│ ├── customer.py
│ ├── product.py
│ └── transaction.py
│── routes/
│ ├── customer_routes.py
│ ├── product_routes.py
│ └── transaction_routes.py
│── data/
│ ├── customers.csv
│ ├── products.csv
│ └── transactions.csv
```

---

## ⚡ API Endpoints

### 👤 Customer
- `POST /login` → Login using `customer_id`  
- `POST /customers` → Add new customer  
- `GET /customers` → Fetch all customers  

### 📦 Product
- `POST /products` → Add new product  
- `GET /products` → Fetch all products  

### 💳 Transaction
- `POST /transactions` → Add transaction  
- `GET /transactions` → Fetch all transactions  

### 🎯 Recommendation
- `POST /recommend`  
  ```json
  {
    "customer_id": 251
  }


