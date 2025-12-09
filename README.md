## Meezan Bank – Retail Management System

A complete retail banking automation platform built using **Flask (Python)**, **HTML/CSS/Jinja**, and **Oracle Database**.
This system simulates real banking operations including **registration**, **authentication**, **deposits**, **fund transfers**, **locker rental**, and **loan management**, fully integrated with PL/SQL stored procedures.

---

## Features

### **User Authentication**

* Register new customers using Oracle stored procedure `CREATE_USER`
* Secure login system (email + password)
* Flask session management

---

###  **Account & Transactions**

* Deposit funds into your own account
* Transfer funds using recipient card number
* View complete transaction history
* Transactions are logged in `BANK_TRANSACTION`
* Integrated with stored procedure `CREATE_TRANSACTION`

---

### **Locker Management**

* View all available lockers
* Rent a locker for 1 year
* Auto-deduct rental fee from user account
* Records stored in `LOCKER_RENTAL`
* Uses stored procedure `RENT_LOCKER` (with fallback manual method)

---

###  **Loan Management**

* Apply for loans from predefined loan types
* View your active loan accounts
* Track pending loan applications
* Repay installments (auto-split into principal + profit)
* Uses Oracle procedures `APPLY_LOAN`, `REPAY_INSTALLMENT`

---

### **User Dashboard**

Displays:

* Account details
* Balance
* Quick actions: Deposit, Transfer, Loan, Locker, Transaction History

---

##  Technology Stack

### **Frontend**

* HTML5
* CSS3
* Jinja2 templating
* Bootstrap styling

### **Backend**

* **Flask Framework**
* Python 3
* DAO-based database access layer
* Session handling

### **Database**

* **Oracle Database 19c**
* PL/SQL procedures & triggers
* Database schema includes:

  * `USER_AUTH`, `CUSTOMER`
  * `ACCOUNT`, `ACCOUNT_HOLDER`
  * `BANK_TRANSACTION`
  * `LOAN_TYPE`, `LOAN_ACCOUNT`, `LOAN_APPLICATION`
  * `LOCKER`, `LOCKER_RENTAL`

---

##  Project Structure

```
/app
 ├── routes/
 │    ├── root/
 │    └── user/
 ├── models/
 ├── templates/
 │    ├── root/
 │    └── user/
 ├── static/
 ├── database.py
 ├── db_utils.py     # DAO layer + Oracle procedure calls
run.py                # App entry points
```

---
## Setup Instructions

### 1️) Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate    # for Windows
```

---

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```



---

### 3️) Configure Oracle Connection

Edit `app/database.py`:

```python
dsn = cx_Oracle.makedsn("localhost", 1521, sid="XE")
username = "your_username"
password = "your_password"
```

---

### 4️) Run the Application

```bash
python run.py
```

App opens at:

```
http://127.0.0.1:5000
```

---


## Learning Outcomes

* Flask + Oracle DB integration
* Calling PL/SQL procedures from Python
* Structuring a full-stack banking system
* DAO design pattern
* Secure session-based authentication
* Implementing banking logic (loans, lockers, transactions)

---

## Team Members

* **Hiba Fatima**
* **Aliza Waris**
* **Zara Asim**

---

## License

This project is built for academic purposes (IBA Karachi).
Not intended for real world financial deployment.

---

