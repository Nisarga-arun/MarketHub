---

# README.md — E-Commerce Web Application

## Internship Project

**Project:** E-Commerce Web Application (Naive Approach)
**Tech Stack:** Python, Flask, Jinja2, MySQL
**Architecture:** Backend + Frontend together

---

## Seed User Credentials

Sample users from `database/seed_data.sql` (for testing):

| Role    | Email               | Password   |
|---------|---------------------|------------|
| Admin   | admin@example.com   | admin123   |
| Staff   | staff@example.com   | staff123   |
| Customer| customer@example.com| customer123|


---

An **E-Commerce system (Electronic Commerce system)** is a software platform that allows businesses to **sell products or services online**.

It enables customers to:

* Browse products
* Add items to a cart
* Place orders
* Make payments
* Track orders

The system manages **products, users, orders, and inventory** digitally.

### Example

Common real-world e-commerce platforms include:

* Amazon
* Flipkart
* Shopify stores
* Small business online shops

In this project, we will build a **simplified e-commerce store** using Flask.

---

An e-commerce platform is used by multiple types of users. Each user has different responsibilities.

## 1. Admin

The **Admin** manages the overall system.

Responsibilities:

* Manage users
* Manage product categories
* Manage stores
* Assign store staff
* Monitor orders and activity

The Admin ensures the platform runs smoothly.

---

## 2. Store Staff (Seller)

Store staff are responsible for managing products and fulfilling orders.

Responsibilities:

* Add new products
* Update product price and quantity
* Upload product images
* View orders received from customers
* Update order status

They manage the store inventory and shipping process.

---

## 3. Customer

Customers use the system to purchase products.

Responsibilities:

* Browse products
* Add items to cart
* Place orders
* View order history
* Track order status

Customers are the **main users of the system**.

---

# 3. Real-Life E-Commerce Flow

The basic workflow of an e-commerce system is:

```
Customer → Product → Cart → Order
```

### Step 1 — Browse Products

Customers visit the website and browse product categories.

Example:

```
Electronics
Clothing
Books
```

---

### Step 2 — View Product

The customer opens a product page to see:

* Product name
* Price
* Description
* Available quantity
* Product image

---

### Step 3 — Add to Cart

If the customer wants to buy the product, they add it to their **shopping cart**.

The cart temporarily stores selected products.

Example cart:

```
Laptop - Qty 1
Mouse - Qty 2
```

---

### Step 4 — Place Order

Once the customer confirms the purchase, the system converts the cart into an **order**.

The order includes:

* Order ID
* Customer details
* Product list
* Total price
* Order status

---

### Step 5 — Order Processing

Store staff receive the order and process it.

Order statuses may include:

```
Placed
Packed
Shipped
Delivered
Cancelled
```

---

# 4. Problems in Manual Selling Systems

Before e-commerce systems existed, stores used manual processes.

These systems had several problems.

## 1. Inventory Errors

Tracking product stock manually often leads to:

* Incorrect stock counts
* Selling unavailable products

---

## 2. Order Management Issues

Orders written on paper can be:

* Lost
* Misinterpreted
* Incorrectly processed

---

## 3. Limited Customer Reach

Physical stores can only sell to **local customers**, while online stores can sell globally.

---

## 4. Time-Consuming Processes

Manual billing and order tracking takes a lot of time.

---

## 5. Poor Data Tracking

It is difficult to track:

* Sales reports
* Popular products
* Customer history

E-commerce systems solve these problems through **automation and digital records**.

---

# 5. Project Scope

To keep this internship project simple, we will build **only the core features** of an e-commerce system.

---

## Features We Will Build

### User Management

* User registration
* Login and logout
* Role-based access

---

### Admin Features

* Manage product categories
* Manage stores
* Manage store staff
* View users

---

### Store Staff Features

* Add products
* Update product details
* Upload product images
* View and update orders

---

### Customer Features

* Browse products
* Add products to cart
* Update cart
* Place orders
* View order history
* Track order status

---

## Features We Will Skip

To keep the system simple, the following advanced features will NOT be implemented.

* Online payment gateway
* Discount coupons
* Product reviews
* Product ratings
* Advanced search
* Notifications
* Multi-vendor marketplace
* Shipping integrations

These features are common in real systems but are **outside the scope of this internship project**.

---

# 6. Summary

In this task, we learned:

* What an e-commerce system is
* Who uses the system
* The workflow of product purchasing
* Problems with manual selling systems
* The scope of our project

---

### Example

An admin might add a new category "Books", create a store "ABC Book Store", and assign a staff member "Ravi" to manage that store.

## Data Admin CAN See

* All users (customers, store staff, other admins) and their details (e.g. name, email, role).
* All product categories and stores.
* All products across all stores (name, price, quantity, images).
* All orders (every customer order from every store).
* Order status and history.
* Which staff is assigned to which store.

## Data Admin CANNOT See

* Customer passwords (stored in encrypted form; no role should see raw passwords).
* Payment card details (we are not implementing payment gateway; if we did, only payment provider would see these).

---

# 2. Store Staff (Seller) Role

**Store staff** manage one or more stores. They handle products and orders for their assigned store(s).

## Store Staff Responsibilities

* **Add new products** — Create product listings (name, price, description, quantity, image) for their store.
* **Update product details** — Change price, quantity, or description when needed.
* **Upload product images** — Add or replace product images.
* **View orders** — See orders placed by customers for their store.
* **Update order status** — Mark orders as Packed, Shipped, or Delivered so customers can track.

### Example

Store staff "Priya" for "Electronics Hub" adds a new product "Wireless Mouse", sets price and stock, and when a customer orders it, she marks the order as "Shipped".

## Data Store Staff CAN See

* Their assigned store(s) and its details.
* Products belonging to their store(s) (name, price, quantity, images).
* Orders placed for their store(s) (order ID, customer info needed for shipping, items, status).
* Product categories (to assign categories to products).

## Data Store Staff CANNOT See

* Other stores' products or orders (only their own store).
* Other users' passwords.
* Full list of all customers across the platform (only customers who ordered from their store).
* Admin-only data (e.g. who else is store staff, other stores' internal details).

---

# 3. Customer Role

**Customers** are the end users who browse products, add to cart, and place orders.

## Customer Responsibilities

* **Browse products** — View product list and categories, open product pages.
* **Add items to cart** — Select products and quantity before checkout.
* **Update cart** — Change quantity or remove items.
* **Place orders** — Confirm the cart and create an order.
* **View order history** — See their past orders.
* **Track order status** — Check if order is Placed, Packed, Shipped, or Delivered.

### Example

A customer "Amit" logs in, browses "Electronics", adds a laptop to the cart, checks out, and later views "My Orders" to see the status as "Shipped".

## Data Customer CAN See

* Product categories and product list (name, price, description, image, availability).
* Their own cart (items and quantities).
* Their own orders (order ID, items, total, status).
* Their own profile (name, email, address if stored).

## Data Customer CANNOT See

* Other customers' orders, carts, or profile data.
* Admin or store staff management screens (categories, stores, user list).
* Other stores' internal data or staff assignments.
* Product management (add/edit/delete products) or order status updates (only view their own status).

---

# 4. Summary

| Role        | Main job                         | Can see                                      | Cannot see                          |
|------------|-----------------------------------|----------------------------------------------|-------------------------------------|
| **Admin**  | Manage platform, users, stores   | All users, categories, stores, products, orders | Raw passwords, payment card details |
| **Store staff** | Manage their store's products & orders | Their store(s), its products, its orders   | Other stores' data, all customers   |
| **Customer**   | Buy products, track orders       | Products, own cart, own orders, own profile  | Others' data, admin/staff screens   |

Defining roles and data access clearly helps you implement **role-based access control** correctly and keep the system secure.

---
