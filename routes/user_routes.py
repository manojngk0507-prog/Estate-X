# routes/user_routes.py
# All user-facing routes: property search, details, booking, wishlist, payment

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import (
    search_properties, get_property_by_id,
    create_booking, get_bookings_by_user, get_booking_by_id, update_payment_status,
    add_to_wishlist, remove_from_wishlist, get_wishlist_by_user, is_in_wishlist,
    get_all_properties
)

user_bp = Blueprint('user', __name__)


def login_required():
    """Return True if a user is logged in."""
    return 'user_id' in session


# ── Home / Property Listing ────────────────────────────────────────────────────

@user_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@user_bp.route('/properties')
def property_list():
    """Property listing page with optional search filters."""
    location  = request.args.get('location', '').strip()
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    bedrooms  = request.args.get('bedrooms', None)

    # Convert numeric filters from string to appropriate types
    min_price = float(min_price) if min_price else None
    max_price = float(max_price) if max_price else None
    bedrooms  = int(bedrooms) if bedrooms else None

    properties = search_properties(location, min_price, max_price, bedrooms)
    return render_template('property_list.html', properties=properties,
                           location=location, min_price=min_price,
                           max_price=max_price, bedrooms=bedrooms)


# ── Property Details ───────────────────────────────────────────────────────────

@user_bp.route('/property/<int:property_id>')
def property_details(property_id):
    """Show full details for a single property."""
    prop = get_property_by_id(property_id)
    if not prop:
        flash('Property not found.', 'error')
        return redirect(url_for('user.property_list'))

    in_wishlist = False
    if login_required():
        in_wishlist = is_in_wishlist(session['user_id'], property_id)

    return render_template('property_details.html', property=prop, in_wishlist=in_wishlist)


# ── Booking ────────────────────────────────────────────────────────────────────

@user_bp.route('/book/<int:property_id>')
def book_property(property_id):
    """Create a booking request for a property."""
    if not login_required():
        flash('Please login to book a property.', 'error')
        return redirect(url_for('auth.login'))

    prop = get_property_by_id(property_id)
    if not prop or prop['status'] == 'Sold':
        flash('This property is not available for booking.', 'error')
        return redirect(url_for('user.property_list'))

    create_booking(session['user_id'], property_id)
    flash('Booking request submitted! The admin will review it shortly.', 'success')
    return redirect(url_for('user.my_bookings'))


@user_bp.route('/my_bookings')
def my_bookings():
    """Show all bookings made by the currently logged-in user."""
    if not login_required():
        flash('Please login to view bookings.', 'error')
        return redirect(url_for('auth.login'))

    bookings = get_bookings_by_user(session['user_id'])
    return render_template('bookings.html', bookings=bookings, is_admin=False)


# ── Payment Simulation ─────────────────────────────────────────────────────────

@user_bp.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    """Simulated payment page for an approved booking."""
    if not login_required():
        flash('Please login.', 'error')
        return redirect(url_for('auth.login'))

    booking = get_booking_by_id(booking_id)
    if not booking or booking['user_id'] != session['user_id']:
        flash('Booking not found.', 'error')
        return redirect(url_for('user.my_bookings'))

    if booking['status'] != 'Approved':
        flash('Payment is only allowed for approved bookings.', 'error')
        return redirect(url_for('user.my_bookings'))

    if request.method == 'POST':
        # Simulate payment – update payment_status to Paid
        update_payment_status(booking_id)
        flash('Payment successful! Your booking is confirmed.', 'success')
        return redirect(url_for('user.payment_success', booking_id=booking_id))

    prop = get_property_by_id(booking['property_id'])
    return render_template('payment.html', booking=booking, property=prop)


@user_bp.route('/payment_success/<int:booking_id>')
def payment_success(booking_id):
    """Payment success confirmation page."""
    if not login_required():
        return redirect(url_for('auth.login'))
    booking = get_booking_by_id(booking_id)
    prop    = get_property_by_id(booking['property_id'])
    return render_template('payment_success.html', booking=booking, property=prop)


# ── Wishlist ───────────────────────────────────────────────────────────────────

@user_bp.route('/wishlist/add/<int:property_id>')
def wishlist_add(property_id):
    if not login_required():
        flash('Please login to use the wishlist.', 'error')
        return redirect(url_for('auth.login'))
    add_to_wishlist(session['user_id'], property_id)
    flash('Property added to wishlist.', 'success')
    return redirect(url_for('user.property_details', property_id=property_id))


@user_bp.route('/wishlist/remove/<int:property_id>')
def wishlist_remove(property_id):
    if not login_required():
        flash('Please login.', 'error')
        return redirect(url_for('auth.login'))
    remove_from_wishlist(session['user_id'], property_id)
    flash('Property removed from wishlist.', 'success')
    return redirect(url_for('user.my_wishlist'))


@user_bp.route('/wishlist')
def my_wishlist():
    if not login_required():
        flash('Please login to view your wishlist.', 'error')
        return redirect(url_for('auth.login'))
    items = get_wishlist_by_user(session['user_id'])
    return render_template('wishlist.html', items=items)
