from django.contrib import admin
from .models import GLCode, Transaction, Employee, Vendor
from import_export.admin import ImportExportModelAdmin
from .resources import GLCodeResource, TransactionResource, EmployeeResource, VendorResource

@admin.register(GLCode)
class GLCodeAdmin(ImportExportModelAdmin):
    resource_class = GLCodeResource
    list_display = ('gl_code', 'gl_description', 'limit', 'limit_utilized', 'balance_available')
    search_fields = ('gl_code', 'gl_description')


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    list_display = ('date', 'gl_code', 'particulars', 'bill_amount', 'utilized_limit', 'remaining_limit')
    list_filter = ('gl_code', 'date')
    search_fields = ('particulars', 'details')
    


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('name', 'designation','address','email','phone_no','created_date','updated_date')
    list_filter = ('designation', 'created_date')
    search_fields = ('email', 'name')
    
    

@admin.register(Vendor)
class VendorAdmin(ImportExportModelAdmin):
    resource_class = VendorResource
    list_display = ('name', 'cnic','type','status','created_date','updated_date')
    list_filter = ('type', 'status')
    search_fields = ('name', 'cnic')