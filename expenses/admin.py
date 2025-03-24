from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GLCode, Transaction, Employee, Vendor, Expense, Region, Branch, CostCenter, Head, SubHead
from .models_user import User, AllowanceRequest
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
    
@admin.register(Expense)
class ExpenseManagementAdmin(admin.ModelAdmin):
    list_display = ('region', 'branch', 'cost_center', 'head', 'sub_head', 'vendor',
                    'payment_mode', 'amount','status','invoice_no', 'created_date')
    
    list_filter = ('region', 'branch', 'status', 'payment_mode')
    search_fields = ('branch__name', 'employee__region')
    
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'region__name')

@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch')
    list_filter = ('branch',)
    search_fields = ('name', 'branch__name')

@admin.register(Head)
class HeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'budget'
)
    
@admin.register(SubHead)
class SubHeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'head')
    list_filter = ('head',)
    search_fields = ('name', 'head__name')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'branch', 'is_staff')
    list_filter = ('role', 'branch', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Information', {'fields': ('role', 'branch')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'branch'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

@admin.register(AllowanceRequest)
class AllowanceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'purpose', 'status', 'requested_date', 'processed_date', 'processed_by')
    list_filter = ('status', 'requested_date', 'processed_date')
    search_fields = ('user__username', 'purpose')
    readonly_fields = ('requested_date',)
    fieldsets = (
        (None, {'fields': ('user', 'amount', 'purpose', 'status')}),
        ('Processing Information', {'fields': ('processed_date', 'processed_by', 'rejection_reason')}),
    )


