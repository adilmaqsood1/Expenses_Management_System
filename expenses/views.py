from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Region, Head, Vendor, Expense, GLCode, Employee
from .models_user import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
import datetime
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

class CustomLoginView(LoginView):
    template_name = 'expenses/login.html'
    redirect_field_name = 'next'
    
    def get_success_url(self):
        # Get the redirect URL from the 'next' parameter if it exists
        redirect_to = self.request.POST.get(self.redirect_field_name, '')
        if not redirect_to:
            # If no redirect URL is provided, redirect based on user role
            if self.request.user.is_admin:
                redirect_to = '/expense/admin/'
            
            elif self.request.user.is_supervisor:
                redirect_to = '/expense/'
            elif self.request.user.is_maker:
                redirect_to = '/expense/'
            else:
                redirect_to = '/mis-dashboard/'
        return redirect_to 
    
class RegisterView(View):
    template_name = 'expenses/register.html'

    def get(self, request):
        return render(request, self.template_name) 


class EmployeeListView(LoginRequiredMixin, View):
    def get(self, request):
        employees_list = Employee.objects.all()
        
        # Apply filters
        name_filter = request.GET.get('name')
        if name_filter:
            employees_list = employees_list.filter(name__icontains=name_filter)
            
        designation_filter = request.GET.get('designation')
        if designation_filter:
            employees_list = employees_list.filter(designation__icontains=designation_filter)
        
        # Get the show parameter from the request, default to showing all entries
        show = request.GET.get('show', '-1')
        
        # If show is not 'All' (-1), paginate the results
        if show != '-1':
            show = int(show)
            paginator = Paginator(employees_list, show)
            page = request.GET.get('page', 1)
            employees = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            # If showing all, no pagination needed
            employees = employees_list
            total_pages = 1
        
        context = {
            'employees': employees,
            'selected_name': name_filter or '',
            'selected_designation': designation_filter or '',
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': employees_list.count()
        }
        
        return render(request, 'expenses/employee_list.html', context)

class AddEmployeeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'expenses/add_employee.html')
    
    def post(self, request):
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        sap_id = request.POST.get('sap_id')
        account = request.POST.get('account')
        account_type = request.POST.get('account_type')
        pls = request.POST.get('pls')
        current = request.POST.get('current')
        
        # Create new employee
        employee = Employee(
            name=name,
            designation=designation,
            address=address,
            email=email,
            phone_no=phone_no,
            sap_id=sap_id,
            account=account,
            account_type=account_type,
            pls=pls,
            current=current
        )
        employee.save()
        
        return redirect('employee_list')

class EditEmployeeView(LoginRequiredMixin, View):
    def get(self, request, employee_id):
        employee = Employee.objects.get(sap_id=employee_id)
        
        context = {
            'employee': employee
        }
        
        return render(request, 'expenses/edit_employee.html', context)
    
    def post(self, request, employee_id):
        employee = Employee.objects.get(sap_id=employee_id)
        
        employee.name = request.POST.get('name')
        employee.designation = request.POST.get('designation')
        employee.address = request.POST.get('address')
        employee.email = request.POST.get('email')
        employee.phone_no = request.POST.get('phone_no')
        employee.sap_id = request.POST.get('sap_id')
        employee.account = request.POST.get('account')
        employee.account_type = request.POST.get('account_type')
        employee.pls = request.POST.get('pls')
        employee.current = request.POST.get('current')
        
        employee.save()
        
        return redirect('employee_list') 



class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        # Get total expenses
        total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate budget utilization
        total_budget = Head.objects.aggregate(Sum('budget'))['budget__sum'] or Decimal('1')
        utilized_budget = Expense.objects.filter(status='Approved').aggregate(Sum('amount'))['amount__sum'] or 0
        budget_utilization = int((utilized_budget / total_budget) * 100) if total_budget > 0 else 0
        
        # Calculate month-over-month change for expenses
        current_month = timezone.now().month
        current_year = timezone.now().year
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_month_year = current_year if current_month > 1 else current_year - 1
        
        current_month_expenses = Expense.objects.filter(
            created_date__month=current_month,
            created_date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        previous_month_expenses = Expense.objects.filter(
            created_date__month=previous_month,
            created_date__year=previous_month_year
        ).aggregate(Sum('amount'))['amount__sum'] or 1  # Avoid division by zero
        
        month_change_percentage = int(((current_month_expenses - previous_month_expenses) / previous_month_expenses) * 100) if previous_month_expenses > 0 else 0
        
        # Get recent activities
        # Recent expenses
        recent_expenses = Expense.objects.all().order_by('-created_date')[:5]
        expense_activities = [{
            'type': 'expense',
            # 'title': f"{expense.sub_head.head.name} Expense",
            'description': f"Added on {expense.created_date.strftime('%B %d, %Y')}",
            'amount': expense.amount,
            'date': expense.created_date,
            'status': expense.status
        } for expense in recent_expenses]
        
        
        # Recent vendors
        recent_vendors = Vendor.objects.all().order_by('-created_date')[:5]
        vendor_activities = [{
            'type': 'vendor',
            'title': f"New Vendor: {vendor.name}",
            'description': f"Added on {vendor.created_date.strftime('%B %d, %Y')}",
            'amount': None,
            'date': vendor.created_date,
            'status': 'New Entry'
        } for vendor in recent_vendors]
        
        # Combine all activities and sort by date
        # Convert datetime objects to date objects for consistent comparison
        for activity in vendor_activities:
            if isinstance(activity['date'], datetime.datetime):
                activity['date'] = activity['date'].date()
                
        all_activities = expense_activities + vendor_activities
        recent_activities = sorted(all_activities, key=lambda x: x['date'], reverse=True)[:5]

        # Get recently processed expenses
        recent_processed = Expense.objects.filter(
            status__in=['Pending', 'Approved', 'Rejected'],
            created_date__gte=timezone.now() - datetime.timedelta(days=30)
        ).order_by('-created_date')[:5]
        
        # Get pending expense approvals count
        pending_expenses = Expense.objects.filter(status='Pending').count()
        
        # Get total employees and vendors count
        employee_count = Employee.objects.count()
        vendor_count = Vendor.objects.filter(disabled=False).count()
        
        # Get recent activities
        recent_expense = Expense.objects.filter(
            created_date__gte=timezone.now() - datetime.timedelta(days=30)
        ).order_by('-created_date')[:5]
        
        expense_activities = [{
            'type': 'expense',
            'title': f"Expense Request {expense.id}",
            'description': f"Created on {expense.created_date.strftime('%B %d, %Y')}",
            'amount': expense.amount,
            'date': expense.created_date,
            'status': expense.status
        } for expense in recent_expenses]
        
        # Get recent employees added/updated
        recent_employees = Employee.objects.all().order_by('-updated_date')[:5]
        employee_activities = [{
            'type': 'employee',
            'title': f"Employee: {employee.name}",
            'description': f"Updated on {employee.updated_date.strftime('%B %d, %Y')}",
            'amount': None,
            'date': employee.updated_date,
            'status': 'Updated'
        } for employee in recent_employees]
        
        # Get recent vendors added/updated
        recent_vendors = Vendor.objects.all().order_by('-updated_date')[:5]
        vendor_activities = [{
            'type': 'vendor',
            'title': f"Vendor: {vendor.name}",
            'description': f"Updated on {vendor.updated_date.strftime('%B %d, %Y')}",
            'amount': None,
            'date': vendor.updated_date,
            'status': 'Updated' if vendor.disabled else 'Active'
        } for vendor in recent_vendors]
        
        # Combine all activities and sort by date
        all_activities = employee_activities + vendor_activities
        recent_activities = sorted(all_activities, key=lambda x: x['date'], reverse=True)[:5]
       
       
        context = {
            'total_expenses': total_expenses,
            'budget_utilization': budget_utilization,
            'month_change_percentage': month_change_percentage,
            'month_change_direction': 'up' if month_change_percentage >= 0 else 'down',
            'recent_activities': recent_activities,
            'pending_expenses': pending_expenses,
            'employee_count': employee_count,
            'vendor_count': vendor_count,
            'recent_processed': recent_processed,
            'recent_activities': recent_activities
        }
        
        return render(request, 'expenses/dashboard.html', context)

class ExpenseListView(LoginRequiredMixin, View):
    def get(self, request):
        # Filter expenses based on user role
        if request.user.is_maker:
            # Makers can only see expenses from their division
            if request.user.division:
                division_name = request.user.division.name
                expenses_list = Expense.objects.filter(division=division_name)
            else:
                expenses_list = Expense.objects.none()
        else:
            # Supervisors and Admins can see all expenses
            expenses_list = Expense.objects.all()
        regions = Region.objects.all()
        # Branches removed
        vendors = Vendor.objects.all()
        heads = Head.objects.all()
        employees = Employee.objects.all()
        payment_modes = dict(Expense.PAYMENT_MODES)
        status_choices = dict(Expense.STATUS_CHOICES)
        
        # Get expense types (Vendor/Employee)
        expense_types = ['Vendor', 'Employee']
        
        # Apply filters
        # Date filters
        start_date = request.GET.get('start_date')
        if start_date:
            expenses_list = expenses_list.filter(created_date__gte=start_date)
            
        end_date = request.GET.get('end_date')
        if end_date:
            expenses_list = expenses_list.filter(created_date__lte=end_date)
        
        # Type filter (not implemented yet as it's not a field in Expense model)
        type_filter = request.GET.get('type')
        
        # Vendor filter
        vendor_filter = request.GET.get('vendor')
        if vendor_filter:
            expenses_list = expenses_list.filter(vendor_id=vendor_filter)
        
        # Employee filter (not implemented yet as it's not a field in Expense model)
        employee_filter = request.GET.get('employee')
        
        # Head filter
        head_filter = request.GET.get('head')
        if head_filter:
            expenses_list = expenses_list.filter(head_id=head_filter)
        
        # GL Code filter
        gl_code_filter = request.GET.get('gl_code')  # Use proper parameter name
        if gl_code_filter:
            expenses_list = expenses_list.filter(gl_code_id=gl_code_filter)
        
        # Region filter
        region_filter = request.GET.get('region')
        if region_filter:
            expenses_list = expenses_list.filter(region_id=region_filter)
        
        
        # Status filter
        status_filter = request.GET.get('status')
        if status_filter:
            expenses_list = expenses_list.filter(status=status_filter)
        
        # Get the show parameter from the request, default to showing all entries
        show = request.GET.get('show', '-1')
        
        # Calculate expense counts by status
        approved_count = expenses_list.filter(status='Approved').count()
        pending_count = expenses_list.filter(status='Pending').count()
        rejected_count = expenses_list.filter(status='Rejected').count()

        # If show is not 'All' (-1), paginate the results
        if show != '-1':
            show = int(show)
            paginator = Paginator(expenses_list, show)
            page = request.GET.get('page', 1)
            expenses = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            # If showing all, no pagination needed
            expenses = expenses_list
            total_pages = 1
        
        context = {
            'expenses': expenses,
            'regions': regions,
            # Branches removed from context
            'vendors': vendors,
            'heads': heads,
            'gl_codes': GLCode.objects.all(),
            'employees': employees,
            'payment_modes': payment_modes,
            'status_choices': status_choices,
            'expense_types': expense_types,
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': expenses_list.count(),
            'approved_count': approved_count,
            'pending_count': pending_count,
            'rejected_count': rejected_count
        }
        return render(request, 'expenses/expense_list.html', context)
        
class ExpenseDetailView(LoginRequiredMixin, View):
    def get(self, request, expense_id):
        try:
            expense = Expense.objects.get(id=expense_id)
            context = {
                'expense': expense
            }
            return render(request, 'expenses/expense_detail.html', context)
        except Expense.DoesNotExist:
            messages.error(request, "Expense not found.")
            return redirect('expense_list')

class AddExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        heads = Head.objects.all()
        vendors = Vendor.objects.all()
        employees = Employee.objects.all()
        payment_modes = dict(Expense.PAYMENT_MODES)
        
        # Filter GL Codes based on user role and division
        if request.user.is_maker:
            # Makers can only see GL codes for their division
            if request.user.division:
                # Here you would implement division-specific GL code filtering
                # This is a placeholder - you would need to add a relation between GLCode and Division
                gl_codes = GLCode.objects.all()
            else:
                gl_codes = GLCode.objects.none()
        else:
            # Supervisors and Admins can see all GL codes
            gl_codes = GLCode.objects.all()
        
        # Get vendor categories for the dropdown
        vendor_categories = dict(Vendor.VENDOR_CATEGORIES)
        
        context = {
            'heads': heads,
            'vendors': vendors,
            'employees': employees,
            'payment_modes': payment_modes,
            'GLCode': gl_codes,
            'vendor_categories': vendor_categories,
            'user_division': request.user.division.name if request.user.division else None,
            'is_maker': request.user.is_maker
        }
        
        return render(request, 'expenses/add_expense.html', context)
    
    def post(self, request):
        # Print form data for debugging
        print("Form data received:", request.POST)
        print("Files received:", request.FILES)
        
        # Get form data
        gl_code_value = request.POST.get('sub_head')  # Field name kept as 'sub_head' for backward compatibility
        expense_type = request.POST.get('type')  # Get the expense type (Vendor/Employee)
        vendor_id = request.POST.get('vendor')
        employee_id = request.POST.get('employee')
        payment_mode = request.POST.get('payment_mode')
        amount = request.POST.get('amount')
        net_amount = request.POST.get('net_amount')
        invoice_no = request.POST.get('invoice_no')
        invoice_date = request.POST.get('invoice_date')
        description = request.POST.get('description')
        invoice_attachment = request.FILES.get('attach_invoice')
        
        # Validate required fields
        missing_fields = []
        if not gl_code_value: missing_fields.append('GL Code')
        if not payment_mode: missing_fields.append('Payment Mode')
        if not amount: missing_fields.append('Amount')
        if not net_amount: missing_fields.append('Net Amount')
        if not invoice_no: missing_fields.append('Invoice Number')
        
        if missing_fields:
            messages.error(request, f"Please fill in all required fields: {', '.join(missing_fields)}")
            return redirect('add_expense')
            
        # Validate expense type and related fields
        if expense_type == 'Vendor' and not vendor_id:
            messages.error(request, "Please select a vendor.")
            return redirect('add_expense')
        elif expense_type == 'Employee' and not employee_id:
            messages.error(request, "Please select an employee.")
            return redirect('add_expense')
        
        # Role-based validation
        if request.user.is_maker:
            # Check if user has a division assigned
            if not request.user.division:
                messages.error(request, "You don't have a division assigned. Please contact an administrator.")
                return redirect('add_expense')
                
            # Validate that the GL code is allowed for this user's division
            try:
                gl_code_obj = GLCode.objects.get(gl_code=gl_code_value)
                # Here you would implement division-specific GL code validation
                # This is a placeholder - you would need to add a relation between GLCode and Division
                # or implement a permission system
                
                # For now, we'll assume all GL codes are valid for demonstration purposes
                # In a real implementation, you would check if this GL code is allowed for the user's division
            except GLCode.DoesNotExist:
                messages.error(request, f"GL Code {gl_code_value} does not exist or is not allowed for your division.")
                return redirect('add_expense')
        
        
        try:
            # Get the GL Code object
            gl_code_obj = GLCode.objects.get(gl_code=gl_code_value)
            
            # Get or create a default Head for the expense
            default_head, _ = Head.objects.get_or_create(
                code=gl_code_obj,
                defaults={'name': gl_code_obj.gl_description, 'budget': 0}
            )
            
            # Set the head to the default head
            head = default_head
            
        except GLCode.DoesNotExist:
            # If GL Code doesn't exist, redirect back with an error message
            messages.error(request, f"GL Code {gl_code_value} does not exist.")
            return redirect('add_expense')
        except Exception as e:
            # If there's an error, redirect back with an error message
            messages.error(request, f"Error processing GL Code: {str(e)}")
            return redirect('add_expense')
        
        # Get vendor based on expense type
        vendor = None
        if expense_type == 'Vendor':
            try:
                vendor = Vendor.objects.get(id=vendor_id) if vendor_id else None
                if not vendor:
                    messages.error(request, "Selected vendor does not exist.")
                    return redirect('add_expense')
            except Vendor.DoesNotExist:
                messages.error(request, "Selected vendor does not exist.")
                return redirect('add_expense')
        else:
            # For Employee type expenses, use a default vendor
            vendor, _ = Vendor.objects.get_or_create(
                name="Employee Expense",
                defaults={'type': 'Individual', 'status': 'Active'}
            )
        
        # Convert string values to appropriate types
        try:
            amount_decimal = Decimal(amount)
            net_amount_decimal = Decimal(net_amount)
        except Exception as e:
            messages.error(request, f"Invalid amount format: {str(e)}")
            return redirect('add_expense')
        
        # Create and save the expense
        try:
            # Check if invoice_date is provided and valid
            if not invoice_date:
                invoice_date = None
                
            # Create the expense object
            expense = Expense(
                # Only include fields that are in the model
                head=head,
                gl_code=gl_code_obj,
                vendor=vendor,  # Always use vendor (default for employee expenses)
                payment_mode=payment_mode,
                amount=amount_decimal,
                net_amount=net_amount_decimal,
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                description=description,
                # Store the user's division and wing information
                division=request.user.division.name if request.user.division else None,
                wing=request.user.wing.name if request.user.wing else None
            )
            
            # Save the expense
            expense.save()
            
            # Add success message and redirect to expenditure claim view
            messages.success(request, 'Expense added successfully! Viewing Expenditure Claim...')
            # Redirect to the expenditure claim view for the newly created expense
            return redirect('budget:expenditure_claim', expense_id=expense.pk)
        except Exception as e:
            # Provide detailed error message
            messages.error(request, f"Error saving expense: {str(e)}")
            return redirect('add_expense')


# New views for GLCode
class GLCodeListView(LoginRequiredMixin, View):
    def get(self, request):
        gl_codes_list = GLCode.objects.all()
        
        # Filtering logic
        code_filter = request.GET.get('gl_code')
        if code_filter:
            gl_codes_list = gl_codes_list.filter(gl_code__icontains=code_filter)
        
        description_filter = request.GET.get('description')
        if description_filter:
            gl_codes_list = gl_codes_list.filter(gl_description__icontains=description_filter)
        
        # Sorting logic
        sort_by = request.GET.get('sort_by', 'gl_code')  # Default sorting by gl_code
        order = request.GET.get('order', 'asc')  # Default order ascending
        
        if order == 'desc':
            gl_codes_list = gl_codes_list.order_by(f'-{sort_by}')
        else:
            gl_codes_list = gl_codes_list.order_by(sort_by)

        # Pagination logic
        show = request.GET.get('show', '-1')
        if show != '-1':
            show = int(show)
            paginator = Paginator(gl_codes_list, show)
            page = request.GET.get('page', 1)
            gl_codes = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            gl_codes = gl_codes_list
            total_pages = 1

        context = {
            'gl_codes': gl_codes,
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': gl_codes_list.count(),
            'sort_by': sort_by,
            'order': order
        }
        return render(request, 'expenses/gl_code_list.html', context)

class AddGLCodeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'expenses/add_gl_code.html')
    
    def post(self, request):
        # Handle form submission
        gl_code = request.POST.get('gl_code')
        gl_description = request.POST.get('gl_description')
        limit_in_millions = request.POST.get('limit_in_millions')
        limit = request.POST.get('limit')
        
        # Check if GL code already exists
        if GLCode.objects.filter(gl_code=gl_code).exists():
            # GL code already exists, return to form with error message
            context = {
                'error': f'GL Code {gl_code} already exists. Please use a different code.',
                'gl_code': gl_code,
                'gl_description': gl_description,
                'limit_in_millions': limit_in_millions,
                'limit': limit
            }
            return render(request, 'expenses/add_gl_code.html', context)
        
        # Create new GL code if it doesn't exist
        GLCode.objects.create(
            gl_code=gl_code,
            gl_description=gl_description,
            limit_in_millions=limit_in_millions if limit_in_millions else None,
            limit=limit if limit else None
        )
        
        return redirect('gl_code_list')

class EditGLCodeView(LoginRequiredMixin, View):
    def get(self, request, gl_code_id):
        try:
            gl_code = GLCode.objects.get(gl_code=gl_code_id)
        except GLCode.DoesNotExist:
            return redirect('gl_code_list')
        
        context = {
            'gl_code': gl_code
        }
        
        return render(request, 'expenses/edit_gl_code.html', context)
    
    def post(self, request, gl_code_id):
        try:
            gl_code = GLCode.objects.get(gl_code=gl_code_id)
        except GLCode.DoesNotExist:
            return redirect('gl_code_list')
        
        # Handle form submission
        gl_code.gl_description = request.POST.get('gl_description')
        limit_in_millions = request.POST.get('limit_in_millions')
        limit = request.POST.get('limit')
        
        gl_code.limit_in_millions = limit_in_millions if limit_in_millions else None
        gl_code.limit = limit if limit else None
        
        gl_code.save()
        
        return redirect('gl_code_list')

class VendorListView(LoginRequiredMixin, View):
    def get(self, request):
        vendors_list = Vendor.objects.all().order_by('id')
        
        # Define vendor type and status choices
        type_choices = [
            ('Individual', 'Individual'),
            ('Company', 'Company'),
            ('Government', 'Government')
        ]
        
        status_choices = [
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ]
        
        # Filter by name
        name_filter = request.GET.get('name')
        if name_filter:
            vendors_list = vendors_list.filter(name__icontains=name_filter)
        
        # Filter by type
        type_filter = request.GET.get('type')
        if type_filter:
            vendors_list = vendors_list.filter(type=type_filter)
            
        # Filter by status
        status_filter = request.GET.get('status')
        if status_filter:
            vendors_list = vendors_list.filter(status=status_filter)
        
        # Get the show parameter from the request, default to showing all entries
        show = request.GET.get('show', '-1')
        
        # If show is not 'All' (-1), paginate the results
        if show != '-1':
            show = int(show)
            paginator = Paginator(vendors_list, show)
            page = request.GET.get('page', 1)
            vendors = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            # If showing all, no pagination needed
            vendors = vendors_list
            total_pages = 1
        
        context = {
            'vendors': vendors,
            'type_choices': dict(type_choices),
            'status_choices': dict(status_choices),
            'selected_name': name_filter or '',
            'selected_type': type_filter or '',
            'selected_status': status_filter or '',
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': vendors_list.count()
        }
        
        return render(request, 'expenses/vendor_list.html', context)

class AddVendorView(LoginRequiredMixin, View):
    def get(self, request):
        # Define vendor type and status choices
        type_choices = [
            ('Individual', 'Individual'),
            ('Company', 'Company'),
            ('Government', 'Government')
        ]
        
        status_choices = [
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ]
        
        context = {
            'type_choices': dict(type_choices),
            'status_choices': dict(status_choices)
        }
        
        return render(request, 'expenses/add_vendor.html', context)
    
    def post(self, request):
        # Handle form submission
        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        type = request.POST.get('type')
        status = request.POST.get('status')
        
        Vendor.objects.create(
            name=name,
            cnic=cnic,
            type=type,
            status=status
        )
        
        return redirect('vendor_list')

class EditVendorView(LoginRequiredMixin, View):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return redirect('vendor_list')
        
        context = {
            'vendor': vendor
        }
        
        return render(request, 'expenses/edit_vendor.html', context)
    
    def post(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return redirect('vendor_list')
        
        # Handle form submission
        vendor.name = request.POST.get('name')
        vendor.cnic = request.POST.get('cnic')
        vendor.type = request.POST.get('type')
        vendor.status = request.POST.get('status')
        vendor.disabled = request.POST.get('disabled') == 'True'
        
        vendor.save()
        
        return redirect('vendor_list')


# Helper: Get GL code details
def get_gl_code_details(gl_code_id):
    gl_code = None
    gl_code_value = ''

    if not gl_code_id:
        return None, ''

    try:
        gl_code = GLCode.objects.filter(gl_code=gl_code_id).first()
        gl_code_value = gl_code.gl_code if gl_code else ''
    except Exception as e:
        logger.exception("Error retrieving GL code")
        gl_code_value = ''

    return gl_code, gl_code_value

# Helper: Get budget limit
def get_budget_limit(expense, gl_code):
    # First try to get budget from Head model associated with this GL code
    if gl_code:
        try:
            head = Head.objects.filter(code=gl_code).first()
            if head and head.budget:
                return head.budget
        except Exception as e:
            print(f"Error fetching head budget: {e}")
            
        # Fallback to GL code's limit fields
        if getattr(gl_code, 'limit', None) is not None:
            return gl_code.limit
        if getattr(gl_code, 'limit_in_millions', None) is not None:
            return Decimal(gl_code.limit_in_millions) * Decimal('1000000')
    
    return Decimal('0.00')

# Helper: Calculate utilized amount before this expense
def get_utilized_before(expense):
    # First try to get utilized budget from Head model
    if expense.gl_code:
        try:
            head = Head.objects.filter(code=expense.gl_code).first()
            if head:
                return head.utilized_budget
        except Exception as e:
            print(f"Error fetching head utilized budget: {e}")
    
    # Fallback to calculating from expenses
    query = Expense.objects.filter(
        status='Approved',
        created_date__year=timezone.now().year
    ).exclude(id=expense.id)

    if expense.gl_code:
        query = query.filter(gl_code=expense.gl_code)

    return query.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

# Helper: Generate PDF response
def generate_pdf_response(template_name, context, filename):
    template = get_template(template_name)
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse('Error generating PDF', status=400)

# Main view
@login_required
def expenditure_claim_view(request, expense_id, *args, **kwargs):
    expense = get_object_or_404(Expense, id=expense_id)
    now = timezone.now().strftime('%Y')
    one_year_ago = str(int(now) - 1)

    gl_code = expense.gl_code
    gl_description = gl_code.gl_description if gl_code else ''
    
    # Get budget information based on GL code
    head = None
    if gl_code:
        head = Head.objects.filter(code=gl_code).first()
    
    # Get budget values
    budget_limit = get_budget_limit(expense, expense.gl_code)
    utilized_before = get_utilized_before(expense)
    available_limit = budget_limit - utilized_before
    net_utilized = utilized_before + expense.amount
    budget_available = budget_limit - net_utilized

    # Additional information
    cost_center_no = ''  # Branch field no longer exists in Expense model
    contact_no = expense.vendor.contact_number if expense.vendor else ''
    contact_person = expense.vendor.name if expense.vendor else ''

    context = {
        'expense': expense,
        'now': now,
        'one_year_ago': one_year_ago,
        'head': head,
        'budget_limit': budget_limit,
        'utilized_before': utilized_before,
        'available_limit': available_limit,
        'net_utilized': net_utilized,
        'budget_available': budget_available,
        'cost_center_no': cost_center_no,
        'contact_no': contact_no,
        'contact_person': contact_person,
        'enable_pdf_download': True
    }

    if request.GET.get('format') == 'pdf':
        return generate_pdf_response('expenses/expenditure_claim.html', context, f'expenditure_claim_{expense_id}.pdf')

    return render(request, 'expenses/expenditure_claim.html', context)