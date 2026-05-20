# MarketHub – E-Commerce Web Application

A multi-role E-Commerce Management System built using Flask and MySQL.

---

## Project Overview

MarketHub is a full-stack web application developed as an internship project.  
The system allows Admins, Store Staff, and Customers to interact with the platform based on their roles.

The application includes product management, category management, cart system, order handling, authentication, and image upload functionality.

---

## Features

### Authentication & Authorization
- User Registration
- User Login & Logout
- Role-Based Access Control
- Session Management

---

### Admin Features
- Manage Users
- Manage Categories
- Manage Stores
- Assign Staff to Stores
- View Orders
- Monitor Platform Activity

---

### Store Staff Features
- Add Products
- Update Product Details
- Upload Product Images
- Manage Inventory
- View Orders
- Update Order Status

---

### Customer Features
- Browse Products
- Add Products to Cart
- Update Cart
- Place Orders
- Track Orders
- View Order History

---

## Technologies Used

### Backend
- Python
- Flask
- Jinja2

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Database
- MySQL

---

## Project Structure

```bash
MarketHub/
│
├── routes/
├── templates/
├── static/
├── database/
├── utils/
├── uploads/
├── app.py
├── requirements.txt
└── README.md
```

---

## System Roles

### Admin
- Manage platform
- Manage users
- Manage categories
- Manage stores
- Assign staff
- Monitor orders

### Store Staff
- Manage products
- Upload images
- Update inventory
- Process orders

### Customer
- Browse products
- Add to cart
- Place orders
- Track orders

---

## E-Commerce Workflow

```text
Customer → Product → Cart → Order
```

### Workflow Steps

1. Customer browses products
2. Customer adds products to cart
3. Customer places order
4. Store staff processes order
5. Order status gets updated

---

## Installation Guide

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/MarketHub.git
```

---

### 2. Move into Project Folder

```bash
cd MarketHub
```

---

### 3. Create Virtual Environment

```bash
python -m venv venv
```

---

### 4. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Configure MySQL Database

Create database in MySQL:

```sql
CREATE DATABASE markethub;
```

Import SQL file:

```bash
database/seed_data.sql
```

---

### 7. Run Application

```bash
python app.py
```

---

## Demo Credentials

| Role     | Email                | Password    |
|----------|----------------------|-------------|
| Admin    | admin@example.com    | admin123    |
| Staff    | staff@example.com    | staff123    |
| Customer | customer@example.com | customer123 |

---

## Screenshots

### Home Page
Add screenshot here

### Admin Dashboard
Add screenshot here

### Product Page
Add screenshot here

### Cart Page
Add screenshot here

---

## Database Features

- User Management
- Product Management
- Category Management
- Order Management
- Cart System
- Inventory Tracking

---

## Security Features

- Password Hashing
- Session Authentication
- Role-Based Authorization
- Protected Routes

---

## Future Enhancements

- Online Payment Gateway
- Product Reviews & Ratings
- Advanced Product Search
- Email Notifications
- Sales Analytics Dashboard
- JWT Authentication
- REST API Integration
- Responsive Mobile UI

---

## Learning Outcomes

Through this project, I learned:

- Flask Framework
- MVC Architecture Basics
- CRUD Operations
- MySQL Integration
- Role-Based Authentication
- Session Management
- File Upload Handling
- E-Commerce Workflow
- Database Design

---

## Challenges Faced

- Managing multiple user roles
- Implementing secure authentication
- Handling image uploads
- Designing database relationships
- Managing cart and order flow

---

## Project Scope

This project focuses on core e-commerce functionalities including:
- Authentication
- Product Management
- Cart System
- Order Processing
- Role Management

Advanced features like payment integration and notifications are outside the scope of this internship project.

---

## Author

### Nisarga Aruna

Internship Project – Flask E-Commerce Application

---

## License

This project is developed for educational and internship purposes.
