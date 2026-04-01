# README – Estate X: Online Property Selling System
# Academic project – Python Flask + MySQL

## Project Structure

```
Estate X/
├── app.py                  # Flask app entry point
├── db_config.py            # MySQL connection config
├── models.py               # All database query functions
├── create_admin.py         # One-time admin account setup script
├── schema.sql              # MySQL database schema (run once)
├── requirements.txt        # Python dependencies
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py      # Login, Register, Logout
│   ├── admin_routes.py     # Admin dashboard, property & booking management
│   └── user_routes.py      # Property listing, booking, wishlist, payment
│
├── templates/
│   ├── base.html           # Shared layout (nav, footer, flash messages)
│   ├── index.html          # Home page
│   ├── login.html          # Login form
│   ├── register.html       # Registration form
│   ├── property_list.html  # Browse + filter properties
│   ├── property_details.html  # Single property view
│   ├── admin_dashboard.html   # Admin control panel
│   ├── add_property.html   # Add property form (admin)
│   ├── edit_property.html  # Edit property form (admin)
│   ├── bookings.html       # Bookings table (admin/user)
│   ├── wishlist.html       # User wishlist
│   ├── payment.html        # Simulated payment form
│   └── payment_success.html  # Payment confirmation page
│
├── static/
│   └── css/
│       └── style.css       # Minimal CSS styling
│
└── uploads/                # Uploaded property images (auto-created)
```

---

## Setup Instructions

### Step 1 – Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 – Set up MySQL Database

1. Open MySQL command line or MySQL Workbench.
2. Run the schema file to create the database and tables:

```sql
SOURCE /path/to/Estate X/schema.sql;
```

Or copy-paste the contents of `schema.sql` directly.

### Step 3 – Configure Database Connection

Edit `db_config.py` and update your MySQL credentials:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",         ← your MySQL username
    password="",         ← your MySQL password
    database="estate_x"
)
```

### Step 4 – Create the Admin Account

```bash
python create_admin.py
```

This creates the admin user:
- **Email:**    admin@estatex.com
- **Password:** admin123

### Step 5 – Run the Application

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Using the System

### Admin Login
- URL: http://localhost:5000/login
- Email: admin@estatex.com
- Password: admin123

### Admin Tasks
1. Login as Admin
2. Go to **Admin Dashboard** → Add / Edit / Delete properties
3. Mark properties as **Verified** or **Sold**
4. Go to **Bookings** → Approve or Reject user bookings

### User Workflow
1. Register a new account → Login
2. Browse **Properties** page, filter by location / price / bedrooms
3. Click **View Details** on a property
4. Click **Book This Property** → booking submitted with status "Pending"
5. Click **Add to Wishlist** to save a property
6. Go to **My Bookings** to track status
7. When status becomes **Approved**, click **Proceed to Payment**
8. Complete simulated payment → status becomes **Paid**

---

## Notes

- Property images are stored in the `uploads/` folder
- Sessions are cookie-based (Flask session)
- Passwords are hashed using Werkzeug's `pbkdf2:sha256`
- The payment system is entirely simulated - no real gateway
- `is_verified` shows a green "Verified" badge on the property
