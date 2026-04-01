# models.py
# Helper functions for database queries (acting as a model layer)

from db_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from datetime import date


# ─────────────────────────────────────────────
#  USER FUNCTIONS
# ─────────────────────────────────────────────

def create_user(name, email, password, phone, role='user'):
    """Insert a new user into the database with a hashed password."""
    hashed = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, %s)",
        (name, email, hashed, phone, role)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_email(email):
    """Fetch a user record by email address."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def verify_password(stored_hash, plain_password):
    """Check whether the provided plain-text password matches the stored hash."""
    return check_password_hash(stored_hash, plain_password)


def get_user_by_id(user_id):
    """Fetch a user record by its primary key."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# ─────────────────────────────────────────────
#  PROPERTY FUNCTIONS
# ─────────────────────────────────────────────

def add_property(title, location, price, description, bedrooms, bathrooms, area, image_path):
    """Insert a new property listing into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO properties
           (title, location, price, description, bedrooms, bathrooms, area, image_path)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (title, location, price, description, bedrooms, bathrooms, area, image_path)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_properties():
    """Return all property records ordered by newest first."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties ORDER BY created_at DESC")
    props = cursor.fetchall()
    cursor.close()
    conn.close()
    return props


def get_property_by_id(property_id):
    """Return a single property record by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties WHERE id = %s", (property_id,))
    prop = cursor.fetchone()
    cursor.close()
    conn.close()
    return prop


def update_property(property_id, title, location, price, description,
                    bedrooms, bathrooms, area, image_path=None):
    """Update fields of an existing property. image_path is optional."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if image_path:
        cursor.execute(
            """UPDATE properties SET title=%s, location=%s, price=%s, description=%s,
               bedrooms=%s, bathrooms=%s, area=%s, image_path=%s WHERE id=%s""",
            (title, location, price, description, bedrooms, bathrooms, area, image_path, property_id)
        )
    else:
        cursor.execute(
            """UPDATE properties SET title=%s, location=%s, price=%s, description=%s,
               bedrooms=%s, bathrooms=%s, area=%s WHERE id=%s""",
            (title, location, price, description, bedrooms, bathrooms, area, property_id)
        )
    conn.commit()
    cursor.close()
    conn.close()


def delete_property(property_id):
    """Permanently delete a property record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = %s", (property_id,))
    conn.commit()
    cursor.close()
    conn.close()


def set_property_status(property_id, status):
    """Update the availability status of a property (Available / Sold)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE properties SET status=%s WHERE id=%s", (status, property_id))
    conn.commit()
    cursor.close()
    conn.close()


def set_property_verified(property_id, is_verified):
    """Mark a property as verified (1) or unverified (0)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE properties SET is_verified=%s WHERE id=%s", (is_verified, property_id))
    conn.commit()
    cursor.close()
    conn.close()


def search_properties(location='', min_price=None, max_price=None, bedrooms=None):
    """Search properties using optional filter parameters."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM properties WHERE status='Available'"
    params = []

    if location:
        query += " AND location LIKE %s"
        params.append(f"%{location}%")

    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)

    if bedrooms is not None:
        query += " AND bedrooms = %s"
        params.append(bedrooms)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    props = cursor.fetchall()
    cursor.close()
    conn.close()
    return props


# ─────────────────────────────────────────────
#  BOOKING FUNCTIONS
# ─────────────────────────────────────────────

def generate_agreement_number():
    """Generate a unique alphanumeric agreement / reference number."""
    return 'AGR-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def create_booking(user_id, property_id):
    """Create a new booking record with status Pending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    agreement = generate_agreement_number()
    cursor.execute(
        """INSERT INTO bookings (user_id, property_id, booking_date, agreement_number)
           VALUES (%s, %s, %s, %s)""",
        (user_id, property_id, date.today(), agreement)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_bookings_by_user(user_id):
    """Return all bookings made by a specific user, with property details."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT b.*, p.title AS property_title, p.location, p.price
           FROM bookings b
           JOIN properties p ON b.property_id = p.id
           WHERE b.user_id = %s
           ORDER BY b.id DESC""",
        (user_id,)
    )
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings


def get_all_bookings():
    """Return all bookings with user and property details (for admin view)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT b.*, u.name AS user_name, u.email AS user_email,
                  p.title AS property_title, p.location, p.price
           FROM bookings b
           JOIN users u ON b.user_id = u.id
           JOIN properties p ON b.property_id = p.id
           ORDER BY b.id DESC"""
    )
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings


def update_booking_status(booking_id, status):
    """Update booking approval status (Approved / Rejected)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # First get the property_id of this booking
    cursor.execute("SELECT property_id FROM bookings WHERE id=%s", (booking_id,))
    res = cursor.fetchone()
    prop_id = res['property_id'] if res else None

    # Update this booking
    cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (status, booking_id))
    conn.commit()
    
    # If approved, mark property as Sold and reject competing pending bookings
    if status == 'Approved' and prop_id:
        cursor.execute("UPDATE properties SET status='Sold' WHERE id=%s", (prop_id,))
        cursor.execute(
            "UPDATE bookings SET status='Rejected' WHERE property_id=%s AND id != %s AND status='Pending'",
            (prop_id, booking_id)
        )
        conn.commit()
        
    cursor.close()
    conn.close()


def get_booking_by_id(booking_id):
    """Return a single booking record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()
    return booking


def update_payment_status(booking_id):
    """Mark the payment for a booking as Paid."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET payment_status='Paid' WHERE id=%s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()


# ─────────────────────────────────────────────
#  WISHLIST FUNCTIONS
# ─────────────────────────────────────────────

def add_to_wishlist(user_id, property_id):
    """Add a property to the user's wishlist (ignore duplicates)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT IGNORE INTO wishlist (user_id, property_id) VALUES (%s, %s)",
        (user_id, property_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def remove_from_wishlist(user_id, property_id):
    """Remove a property from the user's wishlist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM wishlist WHERE user_id=%s AND property_id=%s",
        (user_id, property_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_wishlist_by_user(user_id):
    """Return all wishlist entries for a user, with property details."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT w.id AS wishlist_id, p.*
           FROM wishlist w
           JOIN properties p ON w.property_id = p.id
           WHERE w.user_id = %s
           ORDER BY w.added_at DESC""",
        (user_id,)
    )
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def is_in_wishlist(user_id, property_id):
    """Check whether a property is already in the user's wishlist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM wishlist WHERE user_id=%s AND property_id=%s",
        (user_id, property_id)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None
