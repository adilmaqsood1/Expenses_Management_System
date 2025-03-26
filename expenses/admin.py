from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from .models import GLCode, Region, Branch, CostCenter, Head, SubHead, Vendor, Expense, Transaction
from .models_user import User, AllowanceRequest

# Enhanced Admin Classes

class GLCodeAdmin(ImportExportModelAdmin):
    list_display = ('gl_code', 'gl_description', 'limit', 'limit_utilized', 'balance_available', 'utilization_percentage')
    list_filter = ('gl_description',)
    search_fields = ('gl_code', 'gl_description')
    readonly_fields = ('limit_utilized', 'balance_available')
    
    def utilization_percentage(self, obj):
        if obj.limit and obj.limit > 0:
            percentage = (obj.limit_utilized / obj.limit) * 100 if obj.limit_utilized else 0
            color = 'green'
            if percentage > 70:
                color = 'orange'
            if percentage > 90:
                color = 'red'
            return format_html(
                '<div style="width:100%%; background-color: #f1f1f1; border-radius: 4px;">' 
                '<div style="width:{}%%; background-color: {}; height: 20px; border-radius: 4px; text-align: center; color: white;">' 
                '{:.1f}%</div></div>', 
                min(percentage, 100), color, percentage
            )
        return "N/A"
    utilization_percentage.short_description = 'Utilization'

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch_count')
    search_fields = ('name',)
    
    def branch_count(self, obj):
        return obj.branch_set.count()
    branch_count.short_description = 'Number of Branches'

class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'region')
    list_filter = ('region',)
    search_fields = ('code', 'name')

class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch')
    list_filter = ('branch',)
    search_fields = ('name',)

class HeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'budget', 'subhead_count')
    search_fields = ('code', 'name')
    
    def subhead_count(self, obj):
        return obj.subhead_set.count()
    subhead_count.short_description = 'Number of Sub-Heads'

class SubHeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'head')
    list_filter = ('head',)
    search_fields = ('code', 'name')

class VendorAdmin(ImportExportModelAdmin):
    list_display = ('name', 'cnic', 'type', 'status', 'disabled', 'created_date', 'total_expenses')
    list_filter = ('type', 'status', 'disabled')
    search_fields = ('name', 'cnic')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Vendor Information', {
            'fields': ('name', 'cnic', 'type')
        }),
        ('Status', {
            'fields': ('status', 'disabled')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    def total_expenses(self, obj):
        total = Expense.objects.filter(vendor=obj).aggregate(total=Sum('amount'))['total']
        return f"${total:.2f}" if total else "$0.00"
    total_expenses.short_description = 'Total Expenses'

class ExpenseAdmin(ImportExportModelAdmin):
    list_display = ('invoice_no', 'vendor', 'amount', 'net_amount', 'payment_mode', 'created_date', 'status', 'status_badge')
    list_filter = ('status', 'payment_mode', 'region', 'branch', 'created_date')
    search_fields = ('invoice_no', 'description', 'vendor__name')
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('invoice_no', 'invoice_date', 'vendor', 'description')
        }),
        ('Financial Details', {
            'fields': ('amount', 'withholding_sales_tax', 'withholding_income_tax', 'net_amount', 'payment_mode')
        }),
        ('Categorization', {
            'fields': ('region', 'branch', 'cost_center', 'head', 'sub_head')
        }),
        ('Status', {
            'fields': ('status', 'created_date')
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'Pending': 'orange',
            'Approved': 'green',
            'Rejected': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.status, 'gray'), obj.status
        )
    status_badge.short_description = 'Status'

class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('gl_code', 'date', 'wing_division', 'particulars', 'bill_amount')
    list_filter = ('date', 'gl_code')
    search_fields = ('description', 'wing_division')
    date_hierarchy = 'date'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'branch', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'branch')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Branch Assignment', {
            'fields': ('branch',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

class AllowanceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'purpose', 'status', 'requested_date', 'processed_date', 'processed_by')
    list_filter = ('status', 'requested_date')
    search_fields = ('user__username', 'purpose')
    readonly_fields = ('requested_date',)
    fieldsets = (
        ('Request Details', {
            'fields': ('user', 'amount', 'purpose')
        }),
        ('Status', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Processing', {
            'fields': ('processed_by', 'processed_date', 'requested_date')
        }),
    )

# Register models with custom admin classes
admin.site.register(GLCode, GLCodeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(CostCenter, CostCenterAdmin)
admin.site.register(Head, HeadAdmin)
admin.site.register(SubHead, SubHeadAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AllowanceRequest, AllowanceRequestAdmin)