# 🍽️ Restaurant Management System

A **Flask-based API** for managing restaurant operations, including order processing, cost calculation, and transaction storage. The backend is powered by **Flask** and uses an **SQL database** (SQLite) to store and retrieve data. This system is designed for developers looking to build a backend service with Python and integrate it with a front-end application or mobile interface.

---

## 🔧 Key Features

- 🛒 **Order Management API** – Handle orders with endpoints for adding, updating, and retrieving orders.
- 💵 **Cost Calculation** – Automatically calculate total cost, taxes, and other charges for each order.
- 🧾 **Receipt Generation** – Generate a receipt for each transaction, providing order details and cost breakdown.
- 🗃️ **Database Integration** – Store orders, prices, and transaction data persistently in an **SQLite** database.
- ⚡ **Fast API** – Built with **Flask**, providing a simple and lightweight backend for restaurant management.
  
---

## 🛠️ Tech Stack

- **Python 3**
- **Flask** – Lightweight web framework
- **SQLite3** – Relational database for storing orders and transactions
- **SQLAlchemy** – ORM for database interaction
- **time** and **random** – For order timestamps and unique order numbers

---
## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/BhishanSharma/RestrauntManagementSystem.git
cd RestrauntManagementSystem
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask API Server

```bash
python app.py
```

> ✅ The Flask server will start, and the API will be available on `http://127.0.0.1:5000/`.

---

## API Endpoints

- **GET** `/orders` – Fetch all orders in the system.
- **GET** `/orders/<order_id>` – Retrieve a specific order by its ID.
- **POST** `/orders` – Create a new order.
  - Request Body: 
    ```json
    {
      "order_no": "ORD123",
      "item_name": "Pizza",
      "quantity": 2,
      "price": 10.0
    }
    ```
  - Response:
    ```json
    {
      "order_no": "ORD123",
      "item_name": "Pizza",
      "quantity": 2,
      "price": 10.0,
      "total": 20.0,
      "order_date": "2025-04-19T15:00:00"
    }
    ```

- **PUT** `/orders/<order_id>` – Update an existing order.
- **DELETE** `/orders/<order_id>` – Delete a specific order.

---

## 📁 Project Structure

```
RestrauntManagementSystem/
├── app.py                 # Main Flask application (API routes)
├── models.py              # Database models (SQLAlchemy)
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── restaurant.db          # SQLite database (created at runtime)
```

---

## 📌 Future Enhancements

- [ ] Add **authentication** for secure access (JWT, OAuth)
- [ ] Implement a **frontend interface** to interact with the API
- [ ] Add more detailed order statistics (e.g., sales by item, time-based analysis)
- [ ] **Order history API** for fetching previous orders by customer or date
- [ ] Integrate **payment gateway** for processing transactions

---

## 👨‍💻 Developer

**Bhishan Sharma**  
🔗 [GitHub Profile](https://github.com/BhishanSharma)
