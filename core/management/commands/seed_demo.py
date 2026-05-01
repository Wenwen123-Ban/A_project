from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Seed demo data: admin, students, books, categories, home cards'

    def handle(self, *args, **options):
        from core.models import (
            UserProfile, Book, Category, HomeCard, NewsPost
        )

        with transaction.atomic():
            # ── Admin account ──────────────────────────────────────────
            if not UserProfile.objects.filter(school_id='admin').exists():
                UserProfile.objects.create(
                    school_id='admin', name='Administrator',
                    password='admin', category='Staff',
                    is_staff=True, status='approved',
                    photo='avatar_owl.svg',
                )
                self.stdout.write('[seed] Created admin  (ID: admin / PW: admin)')
            else:
                self.stdout.write('[seed] admin already exists — skipping')

            # ── Demo librarian ─────────────────────────────────────────
            if not UserProfile.objects.filter(school_id='lib01').exists():
                UserProfile.objects.create(
                    school_id='lib01', name='Maria Santos',
                    password='lib123', category='Staff',
                    is_staff=True, status='approved',
                    photo='avatar_fox.svg',
                )
                self.stdout.write('[seed] Created librarian lib01')

            # ── Demo students ──────────────────────────────────────────
            students = [
                ('2024-001', 'Juan Dela Cruz',   'pass123', 'BSIT', '3', 'college', 'avatar_bear.svg'),
                ('2024-002', 'Ana Reyes',         'pass123', 'BSCS', '2', 'college', 'avatar_cat.svg'),
                ('2024-003', 'Carlos Mendoza',    'pass123', 'BSBA', '1', 'college', 'avatar_dog.svg'),
                ('2024-004', 'Liza Bautista',     'pass123', 'BSED', '4', 'college', 'avatar_panda.svg'),
                ('2024-005', 'Miguel Torres',     'pass123', 'BSAM', '2', 'college', 'avatar_rabbit.svg'),
            ]
            for sid, name, pw, course, yr, level, avatar in students:
                if not UserProfile.objects.filter(school_id=sid).exists():
                    UserProfile.objects.create(
                        school_id=sid, name=name, password=pw,
                        category='Student', is_staff=False, status='approved',
                        year_level=yr, school_level=level, course=course,
                        photo=avatar,
                    )
            self.stdout.write('[seed] Demo students ready')

            # ── Book categories ────────────────────────────────────────
            for cat_name in ['General', 'Mathematics', 'Science', 'Literature',
                             'History', 'Technology', 'Philosophy', 'Arts']:
                Category.objects.get_or_create(name=cat_name)
            self.stdout.write('[seed] Categories ready')

            # ── Demo books ─────────────────────────────────────────────
            books = [
                ('BK-001', 'Introduction to Programming',          'Technology'),
                ('BK-002', 'Calculus: Early Transcendentals',      'Mathematics'),
                ('BK-003', 'Noli Me Tangere',                      'Literature'),
                ('BK-004', 'El Filibusterismo',                    'Literature'),
                ('BK-005', 'Philippine History',                   'History'),
                ('BK-006', 'Data Structures and Algorithms',       'Technology'),
                ('BK-007', 'General Physics',                      'Science'),
                ('BK-008', 'Fundamentals of Chemistry',           'Science'),
                ('BK-009', 'The Republic by Plato',               'Philosophy'),
                ('BK-010', 'Business Communication',              'General'),
                ('BK-011', 'Linear Algebra',                       'Mathematics'),
                ('BK-012', 'World History: A Brief Introduction', 'History'),
                ('BK-013', 'Web Development Fundamentals',        'Technology'),
                ('BK-014', 'Environmental Science',               'Science'),
                ('BK-015', 'Filipino Literature Anthology',       'Literature'),
            ]
            added = 0
            for bno, title, cat in books:
                _, created = Book.objects.get_or_create(
                    book_no=bno,
                    defaults={'title': title, 'status': 'Available', 'category': cat}
                )
                if created:
                    added += 1
            self.stdout.write(f'[seed] {added} demo books added')

            # ── Home cards ─────────────────────────────────────────────
            default_cards = [
                (1, 'Library Hours',
                 'Mon–Fri: 7:30 AM – 5:00 PM\nSaturday: 8:00 AM – 12:00 PM\nSunday & Holidays: Closed'),
                (2, 'Borrowing Policy',
                 'Students may borrow up to 3 books at a time.\nBooks are due within 7 days.\nFines apply for overdue items.'),
                (3, 'Reservation Rules',
                 'Reserve online up to 5 books.\nPick up within 3 days of notification.\nUnpicked reservations are automatically cancelled.'),
                (4, 'Contact Us',
                 'Library Desk: local 100\nEmail: library@school.edu\nFacebook: /SchoolLibrary'),
            ]
            for cid, title, body in default_cards:
                HomeCard.objects.get_or_create(
                    card_id=cid,
                    defaults={'title': title, 'body': body}
                )
            self.stdout.write('[seed] Home cards ready')

            # ── Sample news post ───────────────────────────────────────
            if not NewsPost.objects.exists():
                import uuid
                NewsPost.objects.create(
                    post_id=uuid.uuid4().hex,
                    title='Welcome to LBAS — Library Borrowing & Assistance System',
                    summary='The new online reservation system is now live.',
                    body='Students can now reserve books online and collect them at the library desk. '
                         'Log in using your School ID and password. '
                         'Contact the librarian for any assistance.',
                    author='admin',
                )
                self.stdout.write('[seed] Sample news post created')

        self.stdout.write(self.style.SUCCESS('[seed] Done! Admin: ID=admin / PW=admin'))
