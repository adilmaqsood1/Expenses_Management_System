from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0014_remove_employee_branch_delete_branch'),
    ]

    operations = [
        # Skip adding wing field since it already exists from migration 0013
        # This migration is now a no-op (no operation) to avoid the duplicate column error
    ]