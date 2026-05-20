# E-Commerce Web Application — Project Specification

## Project Overview

This project is a simplified E-Commerce Web Application built using:

Python  
Flask  
Jinja2  
MySQL  

The application follows a **monolithic architecture**, where backend logic and frontend templates are managed within the same project.

The system supports three main user roles:

Admin  
Store Staff (Seller)  
Customer  

The goal of this project is to implement the **core workflow of an online store**, including product management, cart functionality, and order processing.

---

# System Workflow

The basic operational flow of the system is:

Customer → Browse Products → Add to Cart → Place Order → Order Processing

1. Customers browse available products.
2. Customers add selected products to a cart.
3. Customers review and place orders.
4. Store staff process the order.
5. Order status is updated until delivery.

---

# System Roles

The system contains three types of users:

Admin  
Store Staff  
Customer

Each role has different responsibilities and system access permissions.

---

# Data Access Rules

## Admin Access

Admin can access:

- All users
- Store information
- Store staff records
- Customer records
- Product categories
- System-level information

Admin manages the overall system configuration.

---

## Store Staff Access

Store staff can access:

- Assigned store information
- Products belonging to their store
- Orders related to their store products

Store staff cannot access:

- Other stores
- System configuration
- Customer account data unrelated to orders

---

## Customer Access

Customers can access:

- Product categories
- Product listings
- Their own cart
- Their own orders
- Their own profile

Customers cannot access:

- Admin pages
- Store staff management
- Other customers’ information
- Store inventory management

---

# Project Tasks

The project is divided into multiple implementation tasks.  
Each task introduces a new part of the system.

---

# Task 1 — Understand E-Commerce Workflow

Define the system workflow and identify the major components required for an online store.

This task establishes the conceptual foundation of the project.

The workflow includes:

- Product browsing
- Cart management
- Order placement
- Order processing

The goal of this task is to understand how the system should behave before implementation begins.

---

# Task 2 — Identify Roles and Responsibilities

Define the roles used in the system and determine the responsibilities of each role.

The roles are:

Admin  
Store Staff  
Customer  

For each role, define:

- Responsibilities
- Data they can access
- Data they cannot access

This task establishes the access control model for the application.

---

# Task 3 — Flask Project Setup

Initialize the Flask application and prepare the project structure.

This task includes:

- Creating the Flask project structure
- Setting up the application entry point
- Configuring environment variables
- Preparing the template and static folders
- Running the development server

The goal is to ensure the application can start successfully.

---

# Task 4 — Database Setup

Configure the MySQL database and connect it to the Flask application.

This task includes:

- Creating the project database
- Configuring database connection settings
- Establishing database connectivity
- Creating a test table
- Verifying that queries can be executed

This task ensures the backend can store and retrieve data.

---

# Task 5 — User Registration and Login

Implement authentication for system users.

This task includes:

- Creating the user database table
- Implementing user registration
- Implementing user login
- Storing encrypted passwords
- Managing login sessions

Users should be able to create accounts and securely log in to the system.

---

# Task 6 — Navigation and Layout

Create common layout components used throughout the application.

This task includes:

- Creating a base template
- Implementing a navigation bar
- Implementing a footer
- Displaying messages for user actions
- Showing role-specific menu options

This task establishes a consistent user interface across pages.

---

# Task 7 — Role Identification

Implement role-based behavior in the system.

This task includes:

- Storing the role in the user table
- Identifying the role of the logged-in user
- Restricting access to certain routes
- Redirecting users based on their role
- Implementing logout functionality

This ensures that each user interacts only with permitted features.

---

# Task 8 — Admin Dashboard

Create the admin dashboard and management views.

This task includes:

- Creating an admin home page
- Displaying user lists
- Displaying store staff records
- Displaying customer records

The admin dashboard provides system-level visibility.

---

# Task 9 — Product Categories

Implement product category management.

This task includes:

- Creating a category data model
- Adding new categories
- Editing existing categories
- Viewing category details
- Listing all categories

Categories organize products within the store.

---

# Task 10 — Store and Staff Management

Implement store creation and staff assignment.

This task includes:

- Creating store records
- Adding store staff
- Assigning staff to stores
- Controlling staff activation status
- Viewing staff lists

When creating staff:

- Email and password must be provided.

When editing staff:

- Email and password fields should not be shown.

---

# Task 11 — Store Staff Dashboard

Create the main interface for store staff.

This task includes:

- Displaying store information
- Viewing products assigned to the store
- Viewing orders received by the store

Store staff manage daily store operations through this dashboard.

---

# Task 12 — Product Management

Implement product management features for store staff.

This task includes:

- Creating product records
- Setting product price
- Managing product quantity
- Uploading product images
- Editing product information
- Viewing product listings

Products belong to specific stores and categories.

---

# Task 13 — Customer Dashboard

Create the customer home interface.

This task includes:

- Displaying profile information
- Browsing product categories
- Viewing product listings

Customers use this dashboard to explore products.

---

# Task 14 — Cart and Order Placement

Implement cart functionality and order creation.

This task includes:

- Adding products to cart
- Updating cart quantities
- Removing products from cart
- Creating orders from the cart
- Displaying order status

Customers can modify the cart before placing an order.

Once the order is placed:

- The cart cannot be modified.

Store staff can update order status but cannot modify order items.

---

# Task 15 — Customer Orders

Implement customer order tracking.

This task includes:

- Displaying customer orders
- Showing upcoming deliveries
- Filtering orders by status
- Viewing order history
- Viewing detailed order information

Customers should be able to track all their purchases.

---

# Project Goal

The final system should support the following workflow:

1. Admin manages categories, stores, and staff.
2. Store staff manage products and process orders.
3. Customers browse products, add items to a cart, and place orders.
4. Store staff update the order status until delivery.