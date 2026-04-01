# routes/admin_routes.py
# All admin-facing routes: dashboard, property management, booking management

import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models import (
    get_all_properties, add_property, get_property_by_id, update_property,
    delete_property, set_property_status, set_property_verified,
    get_all_bookings, update_booking_status
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Allowed image extensions for property uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Return True if the file has an allowed image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required():
    """Check if the current session belongs to an admin user."""
    return session.get('user_role') == 'admin'


# ── Dashboard ──────────────────────────────────────────────────────────────────

@admin_bp.route('/dashboard')
def dashboard():
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))
    properties = get_all_properties()
    bookings   = get_all_bookings()
    return render_template('admin_dashboard.html', properties=properties, bookings=bookings)


# ── Add Property ───────────────────────────────────────────────────────────────

@admin_bp.route('/add_property', methods=['GET', 'POST'])
def add_property_view():
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title       = request.form['title'].strip()
        location    = request.form['location'].strip()
        price       = request.form['price']
        description = request.form['description'].strip()
        bedrooms    = request.form['bedrooms']
        bathrooms   = request.form['bathrooms']
        area        = request.form['area']

        image_path = None
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename   = secure_filename(file.filename)
                upload_dir = os.path.join('uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file.save(os.path.join(upload_dir, filename))
                image_path = filename  # Store only the filename; full path built in template

        add_property(title, location, price, description, bedrooms, bathrooms, area, image_path)
        flash('Property added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_property.html')


# ── Edit Property ──────────────────────────────────────────────────────────────

@admin_bp.route('/edit_property/<int:property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))

    prop = get_property_by_id(property_id)
    if not prop:
        flash('Property not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        title       = request.form['title'].strip()
        location    = request.form['location'].strip()
        price       = request.form['price']
        description = request.form['description'].strip()
        bedrooms    = request.form['bedrooms']
        bathrooms   = request.form['bathrooms']
        area        = request.form['area']

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename   = secure_filename(file.filename)
                upload_dir = os.path.join('uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file.save(os.path.join(upload_dir, filename))
                image_path = filename

        update_property(property_id, title, location, price, description,
                        bedrooms, bathrooms, area, image_path)
        flash('Property updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('edit_property.html', property=prop)


# ── Delete Property ────────────────────────────────────────────────────────────

@admin_bp.route('/delete_property/<int:property_id>')
def delete_property_view(property_id):
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))
    delete_property(property_id)
    flash('Property deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


# ── Toggle Property Status (Available / Sold) ─────────────────────────────────

@admin_bp.route('/toggle_status/<int:property_id>/<string:status>')
def toggle_status(property_id, status):
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))
    set_property_status(property_id, status)
    flash(f'Property marked as {status}.', 'success')
    return redirect(url_for('admin.dashboard'))


# ── Toggle Verified Status ─────────────────────────────────────────────────────

@admin_bp.route('/toggle_verified/<int:property_id>/<int:verified>')
def toggle_verified(property_id, verified):
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))
    set_property_verified(property_id, verified)
    flash('Verification status updated.', 'success')
    return redirect(url_for('admin.dashboard'))


# ── Booking Management ─────────────────────────────────────────────────────────

@admin_bp.route('/bookings')
def bookings():
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))
    all_bookings = get_all_bookings()
    return render_template('bookings.html', bookings=all_bookings, is_admin=True)


@admin_bp.route('/booking_action/<int:booking_id>/<string:action>')
def booking_action(booking_id, action):
    """Approve or Reject a booking request."""
    if not admin_required():
        flash('Admin access required.', 'error')
        return redirect(url_for('auth.login'))

    if action in ('Approved', 'Rejected'):
        update_booking_status(booking_id, action)
        flash(f'Booking {action}.', 'success')
    return redirect(url_for('admin.bookings'))
