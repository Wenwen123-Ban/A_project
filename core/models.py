from django.db import models


class UserProfile(models.Model):
    school_id    = models.CharField(max_length=50, unique=True, db_index=True)
    name         = models.CharField(max_length=150)
    password     = models.CharField(max_length=128)
    category     = models.CharField(max_length=50, default='Student')
    is_staff     = models.BooleanField(default=False)
    status       = models.CharField(max_length=20, default='approved')
    photo        = models.CharField(max_length=200, default='default.png')
    phone_number = models.CharField(max_length=30, blank=True, default='')
    email        = models.CharField(max_length=150, blank=True, default='')
    year_level   = models.CharField(max_length=20, blank=True, default='')
    school_level = models.CharField(max_length=20, blank=True, default='college')
    course       = models.CharField(max_length=100, blank=True, default='N/A')

    class Meta:
        db_table = 'lbas_users'

    def __str__(self):
        return f'{self.school_id} — {self.name}'


class BookRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    book_no = models.CharField(max_length=50, unique=True)
    added_by = models.CharField(max_length=50)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lbas_book_records'

    def __str__(self):
        return str(self.id)


class Book(models.Model):
    book_no  = models.CharField(max_length=50, unique=True, db_index=True)
    title    = models.CharField(max_length=255)
    status   = models.CharField(max_length=20, default='Available')
    category = models.CharField(max_length=100, default='General')
    record_number = models.OneToOneField('BookRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='book')

    class Meta:
        db_table = 'lbas_books'

    def __str__(self):
        return f'{self.book_no} — {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'lbas_categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    name         = models.CharField(max_length=100)
    school_level = models.CharField(max_length=10)  # 'college' or 'jhs'
    is_active    = models.BooleanField(default=True)
    added_by     = models.CharField(max_length=50)
    added_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lbas_courses'
        unique_together = [('name', 'school_level')]

    def __str__(self):
        return f"{self.name} ({self.school_level})"


class Transaction(models.Model):
    book_no          = models.CharField(max_length=50, db_index=True)
    title            = models.CharField(max_length=255, default='')
    school_id        = models.CharField(max_length=50, db_index=True)
    borrower_name    = models.CharField(max_length=150, default='')
    status           = models.CharField(max_length=20, default='Reserved')
    date             = models.DateTimeField(auto_now_add=True)
    expiry           = models.DateField(null=True, blank=True)
    return_date      = models.DateTimeField(null=True, blank=True)
    pickup_schedule  = models.CharField(max_length=100, blank=True, default='')
    pickup_location  = models.CharField(max_length=100, blank=True, default='')
    reservation_note = models.TextField(blank=True, default='')
    phone_number     = models.CharField(max_length=30, blank=True, default='')
    contact_type     = models.CharField(max_length=20, blank=True, default='')
    request_id       = models.CharField(max_length=100, blank=True, default='')
    approved_by      = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        db_table = 'lbas_transactions'

    def __str__(self):
        return f'{self.book_no} / {self.school_id} / {self.status}'


class RegistrationRequest(models.Model):
    request_id     = models.CharField(max_length=60, unique=True)
    request_number = models.CharField(max_length=10, default='0001')
    name           = models.CharField(max_length=150)
    school_id      = models.CharField(max_length=50, db_index=True)
    year_level     = models.CharField(max_length=20, blank=True, default='')
    school_level   = models.CharField(max_length=20, blank=True, default='college')
    course         = models.CharField(max_length=100, blank=True, default='N/A')
    photo          = models.CharField(max_length=200, default='default.png')
    password       = models.CharField(max_length=128, default='')
    status         = models.CharField(max_length=20, default='pending')
    reviewed_by    = models.CharField(max_length=50, blank=True, default='')
    reviewed_at    = models.DateTimeField(null=True, blank=True)
    phone_number   = models.CharField(max_length=30, blank=True, default='')
    email          = models.CharField(max_length=150, blank=True, default='')
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lbas_registration_requests'

    def __str__(self):
        return f'{self.request_id} — {self.name}'


class NewsPost(models.Model):
    post_id        = models.CharField(max_length=60, unique=True)
    title          = models.CharField(max_length=255)
    summary        = models.CharField(max_length=500, blank=True, default='')
    body           = models.TextField(default='')
    image_filename = models.CharField(max_length=200, null=True, blank=True)
    date           = models.DateField(auto_now_add=True)
    author         = models.CharField(max_length=50, default='admin')

    class Meta:
        db_table = 'lbas_news'

    def __str__(self):
        return self.title


class HomeCard(models.Model):
    card_id = models.IntegerField(unique=True)
    title   = models.CharField(max_length=200, default='')
    body    = models.TextField(default='')

    class Meta:
        db_table = 'lbas_home_cards'

    def __str__(self):
        return f'Card {self.card_id}: {self.title}'


class DateRestriction(models.Model):
    date   = models.CharField(max_length=10, unique=True)  # YYYY-MM-DD
    action = models.CharField(max_length=10)  # 'ban' or 'lift'
    reason = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        db_table = 'lbas_date_restrictions'

    def __str__(self):
        return f'{self.date} ({self.action})'
