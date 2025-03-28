from django.db import models
from .models_user import User, AllowanceRequest

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

class Branch(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.code}-{self.name}"

class CostCenter(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Head(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.code}-{self.name}"

class SubHead(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    head = models.ForeignKey(Head, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.code}-{self.name}"

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    
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
    
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    head = models.ForeignKey(Head, on_delete=models.CASCADE)
    sub_head = models.ForeignKey(SubHead, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    withholding_sales_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    withholding_income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    invoice_no = models.CharField(max_length=50, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.invoice_no} - {self.amount}"

class Transaction(models.Model):
    gl_code = models.ForeignKey(GLCode, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    wing_division = models.CharField(max_length=100)
    particulars = models.CharField(max_length=255)
    details = models.TextField()
    bill_amount = models.DecimalField(max_digits=15, decimal_places=2)
    utilized_limit = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_limit = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.particulars} - {self.bill_amount}"

class Employee(models.Model):
    sap_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    account = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)
    pls = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profit Loss Saving")
    current = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name