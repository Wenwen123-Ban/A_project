from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('school_id', models.CharField(db_index=True, max_length=50, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('category', models.CharField(default='Student', max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('status', models.CharField(default='approved', max_length=20)),
                ('photo', models.CharField(default='default.png', max_length=200)),
                ('phone_number', models.CharField(blank=True, default='', max_length=30)),
                ('email', models.CharField(blank=True, default='', max_length=150)),
                ('year_level', models.CharField(blank=True, default='', max_length=20)),
                ('school_level', models.CharField(blank=True, default='college', max_length=20)),
                ('course', models.CharField(blank=True, default='N/A', max_length=100)),
            ],
            options={'db_table': 'lbas_users'},
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('book_no', models.CharField(db_index=True, max_length=50, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(default='Available', max_length=20)),
                ('category', models.CharField(default='General', max_length=100)),
            ],
            options={'db_table': 'lbas_books'},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={'db_table': 'lbas_categories'},
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('book_no', models.CharField(db_index=True, max_length=50)),
                ('title', models.CharField(default='', max_length=255)),
                ('school_id', models.CharField(db_index=True, max_length=50)),
                ('borrower_name', models.CharField(default='', max_length=150)),
                ('status', models.CharField(default='Reserved', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateField(blank=True, null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('pickup_schedule', models.CharField(blank=True, default='', max_length=100)),
                ('pickup_location', models.CharField(blank=True, default='', max_length=100)),
                ('reservation_note', models.TextField(blank=True, default='')),
                ('phone_number', models.CharField(blank=True, default='', max_length=30)),
                ('contact_type', models.CharField(blank=True, default='', max_length=20)),
                ('request_id', models.CharField(blank=True, default='', max_length=100)),
                ('approved_by', models.CharField(blank=True, default='', max_length=50)),
            ],
            options={'db_table': 'lbas_transactions'},
        ),
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('request_id', models.CharField(max_length=60, unique=True)),
                ('request_number', models.CharField(default='0001', max_length=10)),
                ('name', models.CharField(max_length=150)),
                ('school_id', models.CharField(db_index=True, max_length=50)),
                ('year_level', models.CharField(blank=True, default='', max_length=20)),
                ('school_level', models.CharField(blank=True, default='college', max_length=20)),
                ('course', models.CharField(blank=True, default='N/A', max_length=100)),
                ('photo', models.CharField(default='default.png', max_length=200)),
                ('password', models.CharField(default='', max_length=128)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('reviewed_by', models.CharField(blank=True, default='', max_length=50)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=30)),
                ('email', models.CharField(blank=True, default='', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'lbas_registration_requests'},
        ),
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('post_id', models.CharField(max_length=60, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('summary', models.CharField(blank=True, default='', max_length=500)),
                ('body', models.TextField(default='')),
                ('image_filename', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.CharField(default='admin', max_length=50)),
            ],
            options={'db_table': 'lbas_news'},
        ),
        migrations.CreateModel(
            name='HomeCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('card_id', models.IntegerField(unique=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('body', models.TextField(default='')),
            ],
            options={'db_table': 'lbas_home_cards'},
        ),
        migrations.CreateModel(
            name='DateRestriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('date', models.CharField(max_length=10, unique=True)),
                ('action', models.CharField(max_length=10)),
                ('reason', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={'db_table': 'lbas_date_restrictions'},
        ),
    ]
