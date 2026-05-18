# 🛒 E-Commerce Full-Stack System (FastAPI + Streamlit + SQL Server)

A complete **end-to-end E-Commerce system** built using **FastAPI**, **Streamlit**, and **Microsoft SQL Server**, featuring a full backend API, database layer with stored procedures, and an interactive frontend dashboard.

This project demonstrates a real-world production-style architecture including:
- RESTful APIs
- Database design (SQL Server)
- Stored procedures
- Data seeding scripts
- Interactive UI (Streamlit)

---

## 🚀 Project Overview

This system simulates a real E-Commerce platform where users can:
- Register accounts
- Browse products
- Place orders
- View order history
- Analyze sales and top products

The system is split into:
- **Backend API** → Built with FastAPI
- **Frontend UI** → Built with Streamlit
- **Database** → Microsoft SQL Server (schema: `shop`)

---

## 🏗️ System Architecture :

📦 E-Commerce System

 ┣ 📜 main.py  ==>  FastAPI backend
 
 ┣ 📜 app.py   ==>  Streamlit frontend
 
 ┣ 📜 db_setup.py ==>  Database creation scripts
 
 ┣ 📜 seed_data.py  ==> Data insertion scripts
 
 ┣ 📜 SQL Queries/  ==>  SQL schema & procedures



- Frontend communicates with API using HTTP requests
- API handles business logic and database operations
- Database stores users, products, orders, and analytics

---

## 🧰 Tech Stack

- ⚡ Backend: :contentReference[oaicite:0]{index=0}  
- 🎨 Frontend: :contentReference[oaicite:1]{index=1}  
- 🗄️ Database: :contentReference[oaicite:2]{index=2}  
- 🐍 Language: Python  
- 🔗 ORM/DB Tooling: SQLAlchemy + PyODBC  
- 📊 Data Handling: Pandas  
- 🌐 Communication: REST APIs (Requests library)

---

## ✨ Features

### 👤 User Management
- User registration system
- Secure data insertion into database

### 🛍️ Product Management
- View all products
- Add new products
- Categorized product display
- Stock and pricing management

### 📦 Order System
- Create orders
- View user-specific orders
- Order status tracking (pending / shipped / cancelled)

### 📊 Analytics Dashboard
- Top-selling products
- Monthly sales report
- Data visualization using tables

### 🗄️ Database Automation
- Automatic database creation
- Schema setup (`shop`)
- Table creation & constraints
- Stored procedure execution
- Sample data seeding

---

## 📡 API Endpoints

### 👤 Users
- → Register new user

### 🛍️ Products
- → Get all products  
-  → Add new product  

### 📦 Orders
-  → Create order  
-  → Get user orders  
-  → Cancel order  

### 📊 Analytics
- → Top selling products  
-  → Monthly sales report  


🎯 Key Highlights : 

   ==> Full-stack real-world architecture 
     
   => Clean separation between frontend and backend
     
   => SQL Server integration with stored procedures
     
   => Automated database initialization
     
   => Interactive UI with Streamlit cards design
     
   => REST API design using FastAPI
     

📈 Future Improvements : 

   => JWT Authentication system
     
   => Payment gateway integration
     
   => Admin dashboard analytics charts
     
   => Docker deployment
     
   => Cloud hosting (Azure / AWS)
     
   => Role-based access control


👨‍💻 Author : Youssef Ayman
  
   Computer Science & AI Engineer
   
   Specialized in Machine Learning, Backend Systems, and Data Science


⭐ If you like this project:

   Give it a ⭐ on GitHub and feel free to contribute or fork it!


 
