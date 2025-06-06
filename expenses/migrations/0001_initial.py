# Generated by Django 4.2.7 on 2025-05-06 14:55

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('MAKERS', 'Makers'), ('SUPERVISOR', 'Supervisor'), ('MIS', 'MIS')], default='USER', max_length=10)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cadre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Employee Type',
                'verbose_name_plural': ' Employee Types',
            },
        ),
        migrations.CreateModel(
            name='GLCode',
            fields=[
                ('gl_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('gl_description', models.CharField(max_length=255)),
                ('limit_in_millions', models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True)),
                ('limit', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('limit_utilized', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('balance_available', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cnic', models.CharField(blank=True, max_length=15, null=True)),
                ('type', models.CharField(blank=True, choices=[('Individual', 'Individual'), ('Company', 'Company'), ('Government', 'Government')], max_length=50, null=True)),
                ('category', models.CharField(choices=[('General', 'General'), ('Water', 'Water'), ('Electricity', 'Electricity'), ('Internet', 'Internet'), ('Office Supplies', 'Office Supplies')], default='General', max_length=50)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('ntn_number', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=50, null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('wing_division', models.CharField(max_length=100)),
                ('particulars', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('utilized_limit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('remaining_limit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('gl_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='expenses.glcode')),
            ],
        ),
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('fiscal_year', models.CharField(blank=True, max_length=20, null=True)),
                ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('utilized_budget', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('remaining_budget', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_codes', to='expenses.glcode')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.CharField(choices=[('Account', 'Account'), ('Cash', 'Cash'), ('Cheque', 'Cheque')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('net_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('invoice_no', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('wing', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('division', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('supervisor_approval', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('supervisor_remarks', models.TextField(blank=True, null=True)),
                ('supervisor_date', models.DateTimeField(blank=True, null=True)),
                ('admin_approval', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('admin_remarks', models.TextField(blank=True, null=True)),
                ('admin_date', models.DateTimeField(blank=True, null=True)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_approved_expenses', to=settings.AUTH_USER_MODEL)),
                ('gl_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.glcode')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.head')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_expenses', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('sap_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.CharField(max_length=15)),
                ('account_type', models.CharField(blank=True, max_length=100, null=True)),
                ('pls', models.CharField(blank=True, max_length=100, null=True, verbose_name='Profit Loss Saving')),
                ('current', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('cadre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenses.cadre')),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenses.division')),
                ('employee_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenses.employeetype')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.head')),
                ('wing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenses.wing')),
            ],
        ),
        migrations.CreateModel(
            name='AllowanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('purpose', models.TextField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('processed_date', models.DateTimeField(blank=True, null=True)),
                ('approval_reason', models.TextField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowance_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
