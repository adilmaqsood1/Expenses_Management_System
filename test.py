import os
import django
from django.db import connection

# Manually set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_management.settings')  # Replace 'your_project' with your actual project name
django.setup()

def drop_all_tables():
    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        cursor.execute("GRANT ALL ON SCHEMA public TO neondb_owner;")
        cursor.execute("GRANT ALL ON SCHEMA public TO public;")
    print("All tables dropped!")

drop_all_tables()
