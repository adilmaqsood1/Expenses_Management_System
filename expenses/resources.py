from import_export import resources
from .models import GLCode, Employee, Vendor

class GLCodeResource(resources.ModelResource):
    class Meta:
        model = GLCode
        import_id_fields = ('gl_code',) 
        fields = ('gl_code', 'gl_description', 'limit_in_millions', 'limit', 'limit_utilized', 'balance_available')

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('name', 'designation', 'address', 'email', 'phone_no', 'created_date', 'updated_date')

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor
        fields = ('name', 'cnic', 'type', 'status', 'created_date', 'updated_date')