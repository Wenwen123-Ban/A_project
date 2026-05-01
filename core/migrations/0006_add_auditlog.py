from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auditlog_otprequest_problemreport"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("actor_id", models.CharField(max_length=50)),
                ("action", models.CharField(max_length=100)),
                ("target_type", models.CharField(blank=True, max_length=50)),
                ("target_id", models.CharField(blank=True, max_length=100)),
                ("detail", models.TextField(blank=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "lbas_audit_log"},
        ),
    ]
