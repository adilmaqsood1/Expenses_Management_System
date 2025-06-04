from import_export import resources
from .models import GLCode, Employee, Vendor, Head, Expense, Region, Branch, Cadre, EmployeeType, Division, Wing, StationaryRequest

class GLCodeResource(resources.ModelResource):
    def get_import_id_fields(self):
        return ['gl_code'] 
    
    class Meta:
        model = GLCode
        fields = ('gl_code', 'gl_description', 'limit_in_millions', 'limit', 'limit_utilized', 'balance_available')

class EmployeeResource(resources.ModelResource):
    def get_import_id_fields(self):
        return ['sap_id']
        
    class Meta:
        model = Employee
        import_id_fields = ('sap_id',)
        fields = ('sap_id', 'name', 'designation', 'address', 'email', 'phone_no', 'account_number', 'wing', 'division', 'cadre', 'employee_type', 'created_date', 'updated_date')

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor
        import_id_fields = ('name',)
        fields = ('name', 'ntn', 'type', 'category', 'account_number', 'contact_number', 'status', 'created_date', 'updated_date')

class HeadResource(resources.ModelResource):
    class Meta:
        model = Head
        import_id_fields = ('code',)
        fields = ('name', 'code', 'fiscal_year', 'budget', 'utilized_budget', 'remaining_budget')

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense
        import_id_fields = ('invoice_no',)
        fields = ('head', 'gl_code', 'vendor', 'payment_mode', 'amount', 'net_amount', 'invoice_no', 'invoice_date', 'description', 'created_date', 'status', 'wing', 'division', 'created_by', 'supervisor_approval', 'supervisor', 'admin_approval', 'admin')

class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        import_id_fields = ('name',)
        fields = ('name',)

class CadreResource(resources.ModelResource):
    class Meta:
        model = Cadre
        import_id_fields = ('name',)
        fields = ('name', 'description')

class EmployeeTypeResource(resources.ModelResource):
    class Meta:
        model = EmployeeType
        import_id_fields = ('name',)
        fields = ('name', 'description')

class DivisionResource(resources.ModelResource):
    class Meta:
        model = Division
        import_id_fields = ('name',)
        fields = ('name', 'description')

class WingResource(resources.ModelResource):
    class Meta:
        model = Wing
        import_id_fields = ('name', 'division')
        fields = ('name', 'description', 'division')

class StationaryRequestResource(resources.ModelResource):
    class Meta:
        model = StationaryRequest
        import_id_fields = ('user', 'item', 'requested_date')
        fields = ('user', 'item', 'quantity', 'reason', 'requested_date', 'approved_date', 'approved_by', 'status')