from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models_user import User

class GLCode(models.Model):
    gl_code = models.CharField(max_length=20, primary_key=True )
    gl_description = models.CharField(max_length=255)
    limit_in_millions = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    limit_utilized = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    balance_available = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.gl_code} - {self.gl_description}"

class Region(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Head(models.Model):
    name = models.CharField(max_length=255, blank=True)
    code = models.ForeignKey(GLCode, on_delete=models.CASCADE, related_name='head_codes', null=True)
    fiscal_year = models.CharField(max_length=20, blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    utilized_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        # Auto-populate name field with GL code description if empty
        if not self.name and self.code:
            self.name = self.code.gl_description
            
        # Calculate remaining budget before saving
        self.remaining_budget = self.budget - self.utilized_budget
        super().save(*args, **kwargs)
        
    def __str__(self):
        # Changed to return only the name instead of code and name
        return self.name
    
    def update_budget_utilization(self):
        # Calculate utilized budget from expenses that have both supervisor and admin approval
        from django.db.models import Sum
        from decimal import Decimal
        
        utilized = Expense.objects.filter(
            head=self,
            supervisor_approval='Approved',
            admin_approval='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        self.utilized_budget = utilized
        self.remaining_budget = self.budget - self.utilized_budget
        self.save(update_fields=['utilized_budget', 'remaining_budget'])
        
        # Log the update for debugging
        print(f"Updated budget for {self.name}: Budget={self.budget}, Utilized={self.utilized_budget}, Remaining={self.remaining_budget}")
    
    # def __str__(self):
    #     return f"{self.code.gl_code} - {self.name}"


class Vendor(models.Model):
    VENDOR_TYPES = [
        ('Individual', 'Individual'),
        ('Company', 'Company'),
        ('Government', 'Government'),
    ]
    
    VENDOR_CATEGORIES = [
        ('General', 'General'),
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Internet', 'Internet'),
        ('Office Supplies', 'Office Supplies'),
    ]
    
    name = models.CharField(max_length=255)
    ntn = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=50, choices=VENDOR_TYPES, blank=True, null=True)
    category = models.CharField(max_length=50, choices=VENDOR_CATEGORIES, default='General')
    account_number = models.CharField(max_length=255, blank=True, null=True)
    ntn_number = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    
    VENDOR_STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=50, choices=VENDOR_STATUS, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name
        
    @classmethod
    def check_duplicate(cls, name):
        """Check if a vendor with the same name already exists"""
        return cls.objects.filter(name__iexact=name).exists()
        
    @classmethod
    def import_from_excel(cls, excel_file):
        """Import vendors from Excel file"""
        import pandas as pd
        
        df = pd.read_excel(excel_file)
        created_count = 0
        duplicate_count = 0
        error_count = 0
        results = {
            'created': [],
            'duplicates': [],
            'errors': []
        }
        
        for _, row in df.iterrows():
            try:
                # Check required fields
                if 'name' not in row or pd.isna(row['name']):
                    results['errors'].append(f"Row {_ + 2}: Missing vendor name")
                    error_count += 1
                    continue
                    
                # Check for duplicates
                if cls.check_duplicate(row['name']):
                    results['duplicates'].append(row['name'])
                    duplicate_count += 1
                    continue
                    
                # Create new vendor
                vendor = cls(
                    name=row['name'],
                    ntn=row.get('ntn', None) if not pd.isna(row.get('ntn', None)) else None,
                    type=row.get('type', None) if not pd.isna(row.get('type', None)) else None,
                    category=row.get('category', 'General') if not pd.isna(row.get('category', 'General')) else 'General',
                    account_number=row.get('account_number', None) if not pd.isna(row.get('account_number', None)) else None,
                    contact_number=row.get('contact_number', None) if not pd.isna(row.get('contact_number', None)) else None,
                    status=row.get('status', 'Active') if not pd.isna(row.get('status', 'Active')) else 'Active'
                )
                vendor.save()
                results['created'].append(row['name'])
                created_count += 1
            except Exception as e:
                results['errors'].append(f"Row {_ + 2}: {str(e)}")
                error_count += 1
                
        return {
            'created_count': created_count,
            'duplicate_count': duplicate_count,
            'error_count': error_count,
            'results': results
        }

class Branch(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_MODES = [
        ('Account', 'Account'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    # region = models.ForeignKey(Region, on_delete=models.CASCADE)
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    head = models.ForeignKey(Head, on_delete=models.CASCADE)
    gl_code = models.ForeignKey(GLCode, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # withholding_sales_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # withholding_income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    invoice_no = models.CharField(max_length=50, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    wing = models.CharField(max_length=100, blank=True, null=True, default=None)
    division = models.CharField(max_length=100, blank=True, null=True, default=None)
    supervisor_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_expenses')
    supervisor_remarks = models.TextField(blank=True, null=True)
    supervisor_date = models.DateTimeField(null=True, blank=True)
    admin_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_approved_expenses')
    admin_remarks = models.TextField(blank=True, null=True)
    admin_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.invoice_no} - {self.amount}"

# Signal to update Head budget utilization when expense status changes
@receiver(post_save, sender=Expense)
def update_head_budget_on_expense_change(sender, instance, **kwargs):
    # Update the head's budget utilization only when approval status changes
    if instance.head:
        instance.head.update_budget_utilization()

# Signal to update Head budget utilization when expense is deleted
@receiver(post_delete, sender=Expense)
def update_head_budget_on_expense_delete(sender, instance, **kwargs):
    # Update the head's budget utilization if the expense had both approvals
    if instance.head and instance.supervisor_approval == 'Approved' and instance.admin_approval == 'Approved':
        instance.head.update_budget_utilization()



    def __str__(self):
        return f"{self.date} - {self.particulars} - {self.bill_amount}"

class Cadre(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class EmployeeType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Employee Type"
        verbose_name_plural = " Employee Types"
        

class Division(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Wing(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='wings', null=True)

    def __str__(self):
        return self.name

    
class Employee(models.Model):
    sap_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    cadre = models.ForeignKey(Cadre, on_delete=models.CASCADE, null=True, blank=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE, null=True, blank=True)
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    phone_no = models.CharField(max_length=15)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)
    pls = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profit Loss Saving")
    current = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
