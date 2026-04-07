# PartLink - Supplier-Buyer Marketplace

PartLink is a beginner-friendly web platform built with Django that connects small manufacturers (suppliers) with industries (buyers) for small-quantity part orders. The platform allows users with different roles to interact in a marketplace ecosystem.

## Features

- **Role-based Authentication:** Distinct roles for Admins, Suppliers, and Buyers.
- **Supplier Dashboard:** Suppliers can manage their inventory, add products, and see their active stock.
- **Buyer Functionality:** Buyers can browse the marketplace and add products to their orders.
- **Theme Toggle:** Dynamic UI with light and dark mode support.
- **Admin Notifications:** Admins can invite or notify users to become suppliers via email.
- **Sample Data script:** Easily populate the database with default categories, users, and realistic products.

## Technology Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Custom styling with CSS variables), JavaScript (Vanilla)
- **Database:** SQLite (Default, easy to set up for beginners)

## Setup Instructions

1. **Clone or Download the Repository:**
   Ensure you have the project files locally on your machine.
   
2. **Set up a Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate Database (Optional but Recommended):**
   To seed the marketplace with categories, sample suppliers, and items:
   ```bash
   python populate_db.py
   ```

6. **Create a Superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

## Email Configuration

For the Admin Supplier Notification feature to work effectively, you must configure your email credentials.

In `partlink/settings.py`, look for the `Email Configuration` section and update:
```python
EMAIL_HOST_USER = 'your_actual_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = 'your_actual_email@gmail.com'
```

*Note: If using Gmail, you will need to generate an "App Password" via your Google Account's Security settings.*
