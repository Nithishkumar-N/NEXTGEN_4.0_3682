# 🎓 PartLink Architecture & Explanation Guide

This guide is designed to help you completely understand how the **PartLink** project works so you can confidently explain it to your teacher. It breaks down the technologies used, how the code is organized, and how data moves through the application.

---

## 1. Tech Stack Overview

When your teacher asks "what is this built with?", here is your answer:

*   **Backend Framework:** **Python / Django**. Django is a high-level Python framework that helps build secure websites quickly. We chose it because it comes with built-in user authentication and an admin panel, which saves a lot of time.
*   **Database:** **SQLite**. This is a lightweight database that stores everything in a single file (`db.sqlite3`). It requires zero configuration, making it perfect for student projects and local development.
*   **Frontend / UI:** **HTML, CSS, JavaScript**. We didn't use any heavy frontend frameworks like React or Angular. Instead, we used Django's built-in "Templates" to generate HTML, and styled it with pure, modern CSS (using CSS variables for light/dark mode) and standard JS for simple interactivity (like the theme toggle and modals).

---

## 2. Django's "MVT" Architecture (Crucial Concept!)

If there is one thing you must understand, it is **MVT**. Django doesn't use standard MVC (Model View Controller); it uses **Model-View-Template**.

1.  **Model (`models.py`)**: This is your Database structure. Whenever you define a class here (like `Product` or `Order`), Django automatically writes the complex SQL code to create and manage the database tables.
2.  **View (`views.py`)**: This is the brain/logic. When a user clicks a link, the view decides what happens. It pulls data from the *Model* and sends it to the *Template*.
3.  **Template (`.html` files)**: This is what the user sees. It takes the data given by the view and displays it nicely using HTML and CSS.

---

## 3. Project Structure (The "Apps")

Django projects are broken down into smaller, logical pieces called "Apps". If your teacher asks how you organized the code, explain these four main apps:

*   **`partlink/`** (The Core Project Folder):
    *   This holds global settings (`settings.py`) like database config, installed apps, and email setup.
    *   It holds the main URL router (`urls.py`) which directs traffic to the correct app.
*   **`accounts/`** (User Management):
    *   Handles login, registration, and logout.
    *   Contains the `UserProfile` model, which extends the default Django User to classify them as either a **Supplier** or a **Buyer** (and tracks if suppliers are approved).
*   **`products/`** (Inventory):
    *   Contains the `Product` model (Name, price, stock, image).
    *   Handles how suppliers add/edit parts, and how buyers view the part catalog.
*   **`orders/`** (E-commerce Engine):
    *   Contains the `Order` model.
    *   Manages the cart logic, placing an order, and the status lifecycle of an order (Pending → Accepted → Shipped → Delivered).
*   **`dashboard/`** (Control Centers):
    *   This is the hub. Depending on who logs in, `dashboard/views.py` redirects them to one of three places:
        *   **Admin Dashboard:** Platform stats, approve/reject suppliers, global orders, and system-wide notifications.
        *   **Supplier Dashboard:** Managing their own active products, viewing incoming orders, and checking low-stock alerts.
        *   **Buyer Dashboard:** Order history, tracking placed orders, and viewing notifications.

---

## 4. How the Flow Actually Works (A Real Example)

Let's trace what happens when a **Buyer orders a Product**. Explain this flow to your teacher to prove you know how the backend connects to the database:

1.  **The Click (`urls.py`)**: The buyer clicks "Place Order". The URL (`/orders/create/5/`) is mapped in `urls.py` to a specific view function.
2.  **The Logic (`views.py`)**: The `create_order` function kicks in.
    *   It first checks: *Is the user logged in? Are they a buyer?*
    *   It pulls the product data from the database using the `Product` model.
    *   It calculates the total price (Qty × Price).
3.  **The Database (`models.py`)**: The view creates a new `Order` record and saves it to the SQLite database. It marks the status as `"pending"`.
4.  **The Response**: The view redirects the user to their Dashboard, bringing up a success message.
5.  **The Aftermath**: The Supplier logs in, their dashboard view queries the database for "Orders linked to my products", sees the new order, and they click a button to change the status to "Accepted".

---

## 5. Security & Built-in Features Used

Teachers love security and best practices! Mention these points:

*   **Authentication & Authorization:** We used the `@login_required` decorator. If a user tries to access `/dashboard/supplier/` without being logged in, Django kicks them back to the login page automatically.
*   **CSRF Protection:** Every form submission on the site uses `{% csrf_token %}`. This prevents Cross-Site Request Forgery (hackers submitting forms on behalf of users).
*   **Object Relational Mapping (ORM):** We didn't write raw SQL queries like `SELECT * FROM orders`. We used Django's ORM: `Order.objects.filter(buyer=user)`. This prevents SQL Injection attacks by safely sanitizing inputs automatically.

---

## 6. What About APIs? (Crucial for Interviews/Teachers)

If your teacher asks: *"Where is your API?"* or *"Did you use REST APIs?"* 

Your answer should be strongly: **"This application does not use external REST APIs. It is a Server-Side Rendered (SSR) monolithic application."**

Here is how you explain that:
1. **Server-Side Rendering (SSR):** Instead of building a separate API and a separate frontend (like React), our Django backend generates the final HTML itself using **Django Templates** and sends it directly to the user's browser.
2. **Why we chose SSR:** It is significantly faster to develop, much easier to secure (Django handles CSRF and Sessions automatically), and perfect for straightforward marketplace web apps.
3. **Internal API (The ORM):** You *can* mention that Django's ORM (Object-Relational Mapper) acts as an *internal API*. When in `views.py` you write `Product.objects.all()`, that is Django providing a Python "API" to interact with the database without writing raw SQL.

If you ever wanted to build a Mobile App for this project in the future, *then* you would add **Django REST Framework** to build a JSON API. But for this web version, SSR is the best choice!

---

## 7. How to Talk About the "AI Assistance" 🤖

If your teacher knows you used AI, be honest about *how* you used it. It will make you look like an engineer who uses tools efficiently. Say something like:

> *"I configured the core concepts—like deciding to connect Buyers with Suppliers and structuring the approval workflow—but I used AI as an 'intelligent autocomplete'. For example, I knew I needed to filter database records, but the AI helped write the exact Django ORM syntax. I also utilized it heavily for frontend scaffolding (writing the long HTML/CSS boilerplates) so I could spend my time understanding how the backend views and database models connect together."*

### Final Prep:
Before the review, practice opening `dashboard/views.py` and reading the `buyer_dashboard` function line-by-line out loud. If you can roughly explain what that single function does, you'll easily pass any questions!
