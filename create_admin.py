# create_admin.py
# One-time script to create the default admin account in the database.
# Run this ONCE after setting up the database:  python create_admin.py

from werkzeug.security import generate_password_hash
from db_config import get_db_connection

def create_admin():
    """Insert the default admin user with a hashed password."""
    conn   = get_db_connection()
    cursor = conn.cursor()

    # Check if admin already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", ('admin@estatex.com',))
    existing = cursor.fetchone()
    hashed_password = generate_password_hash('admin123')

    if existing:
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, 'admin@estatex.com'))
        conn.commit()
        print("Admin user already exists. Password updated to admin123.")
    else:
        cursor.execute(
            """INSERT INTO users (name, email, password, phone, role)
               VALUES (%s, %s, %s, %s, %s)""",
            ('Admin', 'admin@estatex.com', hashed_password, '9999999999', 'admin')
        )
        conn.commit()
        print("Admin user created successfully!")
        print("  Email   : admin@estatex.com")
        print("  Password: admin123")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_admin()
