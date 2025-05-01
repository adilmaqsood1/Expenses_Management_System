from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from .models import GLCode, Region, Head, Vendor, Expense, Transaction, Employee, GLCode, Cadre, EmployeeType, Division, Wing
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
                '{}</div></div>', 
                min(percentage, 100), color, '{:.1f}%'.format(percentage)
            )
        return "N/A"
    utilization_percentage.short_description = 'Utilization'

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    # Remove branch_count method as Branch model no longer exists
    # def branch_count(self, obj):
    #     return obj.branch_set.count()
    # branch_count.short_description = 'Number of Branches'

class CadreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'budget', 'utilized_budget', 'available_budget', 'utilization_percentage', 'subhead_count')
    search_fields = ('code', 'name')
    readonly_fields = ('utilized_budget', 'available_budget')
    
    def utilized_budget(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            sub_head__head=obj,
            status='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        return format_html("Rs{}", "{:.2f}".format(utilized))
    utilized_budget.short_description = 'Utilized Budget'
    
    def available_budget(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            sub_head__head=obj,
            status='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        available = obj.budget - utilized
        return format_html("Rs{}", "{:.2f}".format(available))
    available_budget.short_description = 'Available Budget'
    
    def utilization_percentage(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            sub_head__head=obj,
            status='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        if obj.budget and obj.budget > 0:
            percentage = (utilized / obj.budget) * 100
            color = 'green'
            if percentage > 70:
                color = 'orange'
            if percentage > 90:
                color = 'red'
            return format_html(
                '<div style="width:100%%; background-color: #f1f1f1; border-radius: 4px;">' 
                '<div style="width:{}%%; background-color: {}; height: 20px; border-radius: 4px; text-align: center; color: white;">' 
                '{}</div></div>', 
                min(percentage, 100), color, '{:.1f}%'.format(percentage)
            )
        return "N/A"
    utilization_percentage.short_description = 'Utilization'
    
    def subhead_count(self, obj):
        return obj.subhead_set.count()
    subhead_count.short_description = 'Number of Sub-Heads'

class VendorTypeFilter(admin.SimpleListFilter):
    title = 'Vendor Type'
    parameter_name = 'type'
    
    def lookups(self, request, model_admin):
        return Vendor.VENDOR_TYPES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset

class VendorStatusFilter(admin.SimpleListFilter):
    title = 'Vendor Status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return Vendor.VENDOR_STATUS
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

class VendorAdmin(ImportExportModelAdmin):
    list_display = ('name', 'cnic', 'type', 'status', 'disabled', 'created_date', 'total_expenses')
    # list_filter = (VendorTypeFilter, VendorStatusFilter, 'disabled')
    search_fields = ('name', 'cnic')
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 25
    fieldsets = (
        ('Vendor Information', {
            'fields': ('name', 'cnic', 'type','status', 'account_number','ntn_number','contact_number','disabled')
        }),
        # ('Status', {
        #     'fields': ('status', 'disabled')
        # }),
        # ('Timestamps', {
        #     'fields': ('created_date', 'updated_date'),
        #     'classes': ('collapse',)
        # }),
    )
    
    def total_expenses(self, obj):
        total = Expense.objects.filter(vendor=obj).aggregate(total=Sum('amount'))['total']
        return "Rs{:.2f}".format(total) if total else "Rs0.00"
    total_expenses.short_description = 'Total Expenses'

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'vendor', 'amount', 'net_amount', 'payment_mode', 'created_date', 'status']
    list_filter = ('status', )
    search_fields = ('invoice_no', 'description', 'vendor__name')
    readonly_fields = ('created_date',)
    fieldsets = (
    ('Expense Details', {
        'fields': (
            'vendor', 'wing', 'division', 'payment_mode',
            'amount', 'net_amount', 'invoice_no', 'invoice_date',
            'description',
        )
    }),
    ('Admin Approval', {
        'fields': (
            'admin_approval', 'admin_remarks'
        )
    }),
)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sub_head":
            # Display GL code and description together
            kwargs["queryset"] = SubHead.objects.all().order_by('code')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def budget_info(self, obj):
        # Display budget information in a formatted way
        return format_html(
            '<div class="budget-info">' 
            '<div class="budget-item"><div class="budget-label">TOTAL HEAD BUDGET</div><div class="budget-value">Loading...</div></div>' 
            '<div class="budget-item"><div class="budget-label">UTILIZED BUDGET</div><div class="budget-value">Loading...</div></div>' 
            '<div class="budget-item"><div class="budget-label">AVAILABLE BUDGET</div><div class="budget-value">Loading...</div></div>' 
            '<div class="budget-item"><div class="budget-label">MONTHLY FINANCIAL LIMIT</div><div class="budget-value">Loading...</div></div>' 
            '</div>'
        )
    budget_info.short_description = 'Budget Information'
    
    class Media:
        js = ('js/expense_form.js',)
        css = {
            'all': ('css/expense_form.css',)
        }
    
    def save_model(self, request, obj, form, change):
        if not obj.admin:
            obj.admin = request.user  # auto-assign admin
        if obj.admin_approval == "Approved" and not obj.admin_date:
            from django.utils import timezone
            obj.admin_date = timezone.now()
        super().save_model(request, obj, form, change)
    
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
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'date_joined')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Account Details', {
            'fields': ('account_name', 'account_number', 'account_type')
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

class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('sap_id', 'name', 'designation', 'email', 'phone_no', 'created_date')
    list_filter = ('designation', 'created_date')
    search_fields = ('sap_id', 'name', 'email', 'phone_no')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Employee Information', {
            'fields': ('sap_id', 'name', 'designation','head', 'address', 'email', 'phone_no', 'branch', 'wing', 'division', 'cadre', 'employee_type')
        }),
        ('Account Details', {
            'fields': ('account_name', 'account_number', 'account_type', 'account', 'pls', 'current')
        }),
        # ('Timestamps', {
        #     'fields': ('created_date', 'updated_date'),
        #     'classes': ('collapse',)
        # }),
    )
    
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class WingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
# Register models with custom admin classes
admin.site.register(GLCode, GLCodeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Head, HeadAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AllowanceRequest, AllowanceRequestAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Cadre, CadreAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Wing, WingAdmin)