"""
SQL-Only Layer for LBAS Defense Demo
All queries use MySQL database only.
Returns empty collections if database is unavailable or empty.
"""
import logging

logger = logging.getLogger("LBAS.dual_db")


def get_books_with_fallback():
    """Get books from MySQL only."""
    try:
        from core.models import Book
        books = list(Book.objects.values('book_no', 'title', 'status', 'category'))
        return books
    except Exception as e:
        logger.error(f"Books: MySQL failed ({e}), returning empty")
        return []


def get_users_with_fallback():
    """Get users from MySQL only."""
    try:
        from core.models import UserProfile
        from api.utils import resolve_photo
        users = [
            {'school_id': u.school_id, 'name': u.name, 'category': u.category,
             'photo': resolve_photo(u.photo), 'status': u.status, 'is_staff': u.is_staff,
             'phone_number': u.phone_number, 'email': getattr(u, 'email', ''),
             'year_level': u.year_level, 'school_level': u.school_level, 'course': u.course}
            for u in UserProfile.objects.filter(is_staff=False)
        ]
        return users
    except Exception as e:
        logger.error(f"Users: MySQL failed ({e}), returning empty")
        return []


def get_admins_with_fallback():
    """Get admins from MySQL only."""
    try:
        from core.models import UserProfile
        from api.utils import resolve_photo
        admins = [
            {'school_id': u.school_id, 'name': u.name, 'category': u.category,
             'photo': resolve_photo(u.photo), 'status': u.status, 'is_staff': True,
             'phone_number': u.phone_number, 'email': getattr(u, 'email', '')}
            for u in UserProfile.objects.filter(is_staff=True)
        ]
        return admins
    except Exception as e:
        logger.error(f"Admins: MySQL failed ({e}), returning empty")
        return []


def get_transactions_with_fallback():
    """Get transactions from MySQL only."""
    try:
        from core.models import Transaction
        txs = list(Transaction.objects.values(
            'id', 'book_no', 'title', 'school_id', 'borrower_name',
            'status', 'date', 'expiry', 'return_date', 'pickup_schedule',
            'pickup_location', 'reservation_note', 'phone_number',
            'contact_type', 'request_id', 'approved_by'
        ))
        return txs
    except Exception as e:
        logger.error(f"Transactions: MySQL failed ({e}), returning empty")
        return []


def get_registration_requests_with_fallback():
    """Get registration requests from MySQL only."""
    try:
        from core.models import RegistrationRequest
        from api.utils import resolve_photo
        reqs = [
            {'request_id': r.request_id, 'request_number': r.request_number,
             'name': r.name, 'school_id': r.school_id, 'year_level': r.year_level,
             'school_level': r.school_level, 'course': r.course,
             'photo': resolve_photo(r.photo), 'status': r.status,
             'reviewed_by': r.reviewed_by, 'phone_number': r.phone_number,
             'email': r.email, 'created_at': str(r.created_at)[:16]}
            for r in RegistrationRequest.objects.all().order_by('-created_at')
        ]
        return reqs
    except Exception as e:
        logger.error(f"RegRequests: MySQL failed ({e}), returning empty")
        return []


def get_categories_with_fallback():
    """Get categories from MySQL only."""
    try:
        from core.models import Category
        cats = list(Category.objects.values_list('name', flat=True))
        return sorted(cats) if cats else []
    except Exception as e:
        logger.error(f"Categories: MySQL failed ({e}), returning empty")
        return []
