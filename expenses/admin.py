from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from .models import GLCode, Region, Head, Vendor, Expense, Employee, GLCode, Cadre, EmployeeType, Division, Wing
from .models_user import User

# Enhanced Admin Classes

class GLCodeAdmin(ImportExportModelAdmin):
    list_display = ('gl_code', 'gl_description', 'limit', 'limit_utilized', 'balance_available', 'utilization_percentage')
    list_filter = ('gl_description',)
    search_fields = ('gl_code', 'gl_description')
    readonly_fields = ('limit_utilized', 'balance_available')
    list_per_page = 25
    
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
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('gl_code')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 25
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('name')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class CadreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 25
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('name')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 25
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('name')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class HeadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name','budget', 'utilized_budget', 'available_budget', 'utilization_percentage', 'gl_code_count')
    search_fields = ('code__gl_code',)
    readonly_fields = ('utilized_budget', 'available_budget')
    list_per_page = 25
    fieldsets = (
        (None, {
            "fields": (
                'code', 'name','budget', 'fiscal_year'
            ),
        }),
    )
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Add JavaScript to auto-populate name field with GL code description
        if 'code' in form.base_fields:
            form.base_fields['code'].widget.attrs['onchange'] = 'updateNameField(this.value)'
            
            # Add the JavaScript function to the page
            from django.forms.widgets import Media
            form.Media = Media(js=('js/head_admin.js',))
            
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "code":
            # Display only GL code without description
            from django.forms.models import ModelChoiceField
            from .models import GLCode
            
            class GLCodeModelChoiceField(ModelChoiceField):
                def label_from_instance(self, obj):
                    return f"{obj.gl_code} - {obj.gl_description}"
            
            kwargs["queryset"] = GLCode.objects.all().order_by('gl_code')
            kwargs["form_class"] = GLCodeModelChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def utilized_budget(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            head=obj,
            supervisor_approval='Approved',
            admin_approval='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        return format_html("Rs{}", "{:.2f}".format(utilized))
    utilized_budget.short_description = 'Utilized Budget'
    
    def available_budget(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            head=obj,
            supervisor_approval='Approved',
            admin_approval='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        available = obj.budget - utilized
        return format_html("Rs{}", "{:.2f}".format(available))
    available_budget.short_description = 'Available Budget'
    
    def utilization_percentage(self, obj):
        from django.db.models import Sum
        from decimal import Decimal
        utilized = Expense.objects.filter(
            head=obj,
            supervisor_approval='Approved',
            admin_approval='Approved'
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
    
    def gl_code_count(self, obj):
        # Count related GL codes through expenses
        return Expense.objects.filter(head=obj).values('gl_code').distinct().count()
    gl_code_count.short_description = 'Number of GL Codes'
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('code')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'
    
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
    list_per_page = 25
    
    def lookups(self, request, model_admin):
        return Vendor.VENDOR_STATUS
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

class VendorAdmin(ImportExportModelAdmin):
    list_display = ('name', 'ntn', 'type', 'status',)
    list_filter = ('name', 'status',)
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('name', 'ntn', 'type', 'status', 'account_number', 'contact_number', 'disabled')
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
        return "Rs{:}".format(total) if total else "Rs0"
    total_expenses.short_description = 'Total Expenses'
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('id')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'
    
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('sap_id', 'name', 'designation', 'wing', 'division', 'cadre')
    list_filter = ('designation', 'created_date')
    search_fields = ('sap_id', 'name', 'email', 'phone_no')
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 25
    fieldsets = (
        ('Employee Information', {
            'fields': ('sap_id', 'name', 'designation', 'address', 'email', 'phone_no', 'wing', 'division', 'cadre', 'employee_type')
        }),
        ('Account Details', {
            'fields': ( 'pls', 'current')
        }),
    )
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('sap_id')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'vendor', 'amount', 'net_amount', 'payment_mode', 'invoice_date', 'status']
    list_filter = ('status', )
    search_fields = ('expense', 'description', 'vendor__name')
    readonly_fields = ('created_date',)
    list_per_page = 25
    fieldsets = (
    ('Expense Details', {
        'fields': (
            'vendor', 'head', 'gl_code', 'wing', 'division', 'payment_mode',
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
        if db_field.name == "gl_code":
            # Display GL code and description together
            kwargs["queryset"] = GLCode.objects.all().order_by('gl_code')
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
            
        # Update the status field based on admin_approval
        if obj.admin_approval in ["Approved", "Rejected"]:
            obj.status = obj.admin_approval
            
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
    
    def get_queryset(self, request):
        self.request = request
        self._serial_queryset = super().get_queryset(request).order_by('invoice_no')  # Descending order
        self._serial_index_map = {obj.pk: idx + 1 for idx, obj in enumerate(self._serial_queryset)}
        return self._serial_queryset

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        return self._serial_index_map.get(obj.pk, "-")

    get_serial_number.short_description = 'Sr. No'
        

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_per_page = 20  # Optional: number of rows per page

    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'division', 'wing','first_name', 'last_name', 'date_joined')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Account Details', {
            'fields': ('account_number', 'account_type')
        }),
    )

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('username')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'


    
class WingInline(admin.TabularInline):
    model = Wing
    extra = 1
    fields = ('name', 'description')

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'wing_count')
    list_per_page = 20
    inlines = [WingInline]
    
    def wing_count(self, obj):
        return obj.wings.count()
    wing_count.short_description = 'Wings'
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('name')  # Fixed ordering for serial number

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

class WingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_per_page = 25
    
    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        return qs.order_by('name')  

    def get_list_display(self, request):
        return ('get_serial_number',) + tuple(super().get_list_display(request))

    def get_serial_number(self, obj):
        queryset = self.get_queryset(self.request)
        return list(queryset).index(obj) + 1

    get_serial_number.short_description = 'Sr. No'

    
# Register models with custom admin classes
admin.site.register(GLCode, GLCodeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Head, HeadAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Cadre, CadreAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(Wing, WingAdmin)
admin.site.register(Division, DivisionAdmin)