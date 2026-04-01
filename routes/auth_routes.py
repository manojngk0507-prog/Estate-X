# routes/auth_routes.py
# Handles user registration and login/logout

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import create_user, get_user_by_email, verify_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Show registration form and handle new user creation."""
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip()
        password = request.form['password']
        phone    = request.form['phone'].strip()

        # Check if email already exists
        existing = get_user_by_email(email)
        if existing:
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('auth.register'))

        create_user(name, email, password, phone)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form and authenticate user credentials."""
    if request.method == 'POST':
        email    = request.form['email'].strip()
        password = request.form['password']

        user = get_user_by_email(email)
        if user and verify_password(user['password'], password):
            # Store minimal info in session
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.property_list'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Clear the session and redirect to home."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
