"""
LBAS Data Store — SQL-Only Backend.
All reads and writes use MySQL database exclusively.
Returns empty collections on database errors.
"""
import logging

logger = logging.getLogger("LBAS.store")


# ── Database health check ────────────────────────────────────────

def check_mysql():
    """Verify database connection is working."""
    try:
        from django.db import connection
        connection.ensure_connection()
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def mysql_ok():
    """Quick health check without raising exceptions."""
    return check_mysql()


# ── SQL-Only Read Functions (used by API endpoints) ────────────────

def get_books():
    """Get all books from database."""
    try:
        from core.models import Book
        from django.forms.models import model_to_dict
        books = [model_to_dict(b, fields=['book_no', 'title', 'status', 'category']) 
                 for b in Book.objects.all()]
        return books
    except Exception as e:
        logger.error(f"get_books: {e}")
        return []


def get_users():
    """Get all regular users (not staff) from database."""
    try:
        from core.models import UserProfile
        from api.utils import resolve_photo
        from django.forms.models import model_to_dict
        users = [
            {
                'school_id': u.school_id,
                'name': u.name,
                'category': u.category,
                'photo': resolve_photo(u.photo),
                'status': u.status,
                'is_staff': False,
                'phone_number': u.phone_number,
                'email': getattr(u, 'email', ''),
                'year_level': u.year_level,
                'school_level': u.school_level,
                'course': u.course,
            }
            for u in UserProfile.objects.filter(is_staff=False)
        ]
        return users
    except Exception as e:
        logger.error(f"get_users: {e}")
        return []


def get_admins():
    """Get all admin users from database."""
    try:
        from core.models import UserProfile
        from api.utils import resolve_photo
        admins = [
            {
                'school_id': u.school_id,
                'name': u.name,
                'category': u.category,
                'photo': resolve_photo(u.photo),
                'status': u.status,
                'is_staff': True,
                'phone_number': u.phone_number,
                'email': getattr(u, 'email', ''),
                'year_level': getattr(u, 'year_level', ''),
                'school_level': getattr(u, 'school_level', ''),
                'course': getattr(u, 'course', ''),
            }
            for u in UserProfile.objects.filter(is_staff=True)
        ]
        return admins
    except Exception as e:
        logger.error(f"get_admins: {e}")
        return []


def get_transactions():
    """Get all transactions from database."""
    try:
        from core.models import Transaction
        from django.forms.models import model_to_dict
        txs = [model_to_dict(t, fields=[
            'id', 'book_no', 'title', 'school_id', 'borrower_name',
            'status', 'date', 'expiry', 'return_date', 'pickup_schedule',
            'pickup_location', 'reservation_note', 'phone_number',
            'contact_type', 'request_id', 'approved_by'
        ]) for t in Transaction.objects.all()]
        return txs
    except Exception as e:
        logger.error(f"get_transactions: {e}")
        return []


def get_registration_requests():
    """Get all registration requests from database."""
    try:
        from core.models import RegistrationRequest
        from api.utils import resolve_photo
        reqs = [
            {
                'request_id': r.request_id,
                'request_number': r.request_number,
                'name': r.name,
                'school_id': r.school_id,
                'year_level': r.year_level,
                'school_level': r.school_level,
                'course': r.course,
                'photo': resolve_photo(r.photo),
                'status': r.status,
                'reviewed_by': r.reviewed_by,
                'phone_number': r.phone_number,
                'email': r.email,
                'created_at': str(r.created_at)[:16]
            }
            for r in RegistrationRequest.objects.all().order_by('-created_at')
        ]
        return reqs
    except Exception as e:
        logger.error(f"get_registration_requests: {e}")
        return []


def get_categories():
    """Get all book categories from database."""
    try:
        from core.models import Category
        cats = sorted(list(Category.objects.values_list('name', flat=True)))
        return cats if cats else ['General', 'Mathematics', 'Science', 'Literature']
    except Exception as e:
        logger.error(f"get_categories: {e}")
        return ['General', 'Mathematics', 'Science', 'Literature']


def find_user(school_id):
    """Find user by school_id (admin or regular user)."""
    try:
        from core.models import UserProfile
        sid = str(school_id).strip().lower()
        user = UserProfile.objects.get(school_id=sid)
        return {
            'school_id': user.school_id,
            'name': user.name,
            'category': user.category,
            'status': user.status,
            'is_staff': user.is_staff,
            'phone_number': user.phone_number,
            'email': getattr(user, 'email', ''),
            'year_level': getattr(user, 'year_level', ''),
            'school_level': getattr(user, 'school_level', ''),
            'course': getattr(user, 'course', ''),
        }
    except Exception as e:
        logger.debug(f"find_user({school_id}): {e}")
        return None


# ── JSON compatibility stubs ─────────────────────────────────────
# These exist for backward-compatibility with code that called the
# old JSON file store. With MySQL/SQLite as primary DB they are
# safe no-ops that return empty lists.

def jread(key):
    """Legacy JSON store read — returns empty list (DB is source of truth)."""
    return []


def jwrite(key, data):
    """Legacy JSON store write — no-op (DB is source of truth)."""
    pass


def sync_to_mysql():
    """Legacy sync helper — no-op (data already lives in DB)."""
    pass
