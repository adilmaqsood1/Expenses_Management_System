from django.db import models
from django.shortcuts import render, redirect
from django.views import View
from .models import Region, Branch, CostCenter, Head, SubHead, Vendor, Expense, GLCode, Transaction, Employee
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
import datetime
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator

class CustomLoginView(LoginView):
    template_name = 'expenses/login.html'
    redirect_field_name = 'next'
    
    def get_success_url(self):
        # Get the redirect URL from the 'next' parameter if it exists
        redirect_to = self.request.POST.get(self.redirect_field_name, '')
        if not redirect_to:
            # If no redirect URL is provided, redirect based on user role
            if self.request.user.is_admin:
                redirect_to = '/admin/'
            
            elif self.request.user.is_editor:
                redirect_to = '/allowance-requests/'
            elif self.request.user.role=='User':
                redirect_to = '/expenses/'
            else:
                redirect_to = '/'
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
        
        # Get pending approvals count
        from .models_user import AllowanceRequest
        expense_pending = Expense.objects.filter(status='Pending').count()
        allowance_pending = AllowanceRequest.objects.filter(status='PENDING').count()
        pending_approvals = expense_pending + allowance_pending
        
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
            'title': f"{expense.head.name} Expense",
            'description': f"Added by {request.user.username} on {expense.created_date.strftime('%B %d, %Y')}",
            'amount': expense.amount,
            'date': expense.created_date,
            'status': expense.status
        } for expense in recent_expenses]
        
        # Recent transactions
        recent_transactions = Transaction.objects.all().order_by('-date')[:5]
        transaction_activities = [{
            'type': 'transaction',
            'title': transaction.particulars,
            'description': f"Transaction on {transaction.date.strftime('%B %d, %Y')}",
            'amount': transaction.bill_amount,
            'date': transaction.date,
            'status': 'Completed'
        } for transaction in recent_transactions]
        
        # Recent allowance requests
        from .models_user import AllowanceRequest
        recent_allowances = AllowanceRequest.objects.all().order_by('-requested_date')[:5]
        allowance_activities = [{
            'type': 'allowance',
            'title': f"Allowance Request",
            'description': f"Requested by {allowance.user.username} on {allowance.requested_date.strftime('%B %d, %Y')}",
            'amount': allowance.amount,
            'date': allowance.requested_date,
            'status': allowance.status
        } for allowance in recent_allowances]
        
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
                
        all_activities = expense_activities + transaction_activities + vendor_activities
        recent_activities = sorted(all_activities, key=lambda x: x['date'], reverse=True)[:5]
        
        # Get user's allowance requests for dashboard updates
        user_allowance_requests = []
        pending_requests_count = 0
        approved_requests_count = 0
        rejected_requests_count = 0
        
        if request.user.is_subhead:
            user_allowance_requests = AllowanceRequest.objects.filter(user=request.user).order_by('-requested_date')
            pending_requests_count = user_allowance_requests.filter(status='PENDING').count()
            approved_requests_count = user_allowance_requests.filter(status='APPROVED').count()
            rejected_requests_count = user_allowance_requests.filter(status='REJECTED').count()
        
        context = {
            'total_expenses': total_expenses,
            'pending_approvals': pending_approvals,
            'budget_utilization': budget_utilization,
            'month_change_percentage': month_change_percentage,
            'month_change_direction': 'up' if month_change_percentage >= 0 else 'down',
            'recent_activities': recent_activities,
            'user_allowance_requests': user_allowance_requests,
            'pending_requests_count': pending_requests_count,
            'approved_requests_count': approved_requests_count,
            'rejected_requests_count': rejected_requests_count
        }
        
        return render(request, 'expenses/dashboard.html', context)

class ExpenseListView(LoginRequiredMixin, View):
    def get(self, request):
        expenses_list = Expense.objects.all()
        regions = Region.objects.all()
        branches = Branch.objects.all()
        cost_centers = CostCenter.objects.all()
        vendors = Vendor.objects.all()
        heads = Head.objects.all()
        sub_heads = SubHead.objects.all()
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
        
        # Sub-head filter
        sub_head_filter = request.GET.get('sub_head')
        if sub_head_filter:
            expenses_list = expenses_list.filter(sub_head_id=sub_head_filter)
        
        # Region filter
        region_filter = request.GET.get('region')
        if region_filter:
            expenses_list = expenses_list.filter(region_id=region_filter)
        
        # Branch filter
        branch_filter = request.GET.get('branch')
        if branch_filter:
            expenses_list = expenses_list.filter(branch_id=branch_filter)
        
        # Cost center filter
        cost_center_filter = request.GET.get('cost_center')
        if cost_center_filter:
            expenses_list = expenses_list.filter(cost_center_id=cost_center_filter)
        
        # Status filter
        status_filter = request.GET.get('status')
        if status_filter:
            expenses_list = expenses_list.filter(status=status_filter)
        
        # Get the show parameter from the request, default to showing all entries
        show = request.GET.get('show', '-1')
        
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
            'branches': branches,
            'cost_centers': cost_centers,
            'vendors': vendors,
            'heads': heads,
            'sub_heads': sub_heads,
            'employees': employees,
            'payment_modes': payment_modes,
            'status_choices': status_choices,
            'expense_types': expense_types,
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': expenses_list.count()
        }
        return render(request, 'expenses/expense_list.html', context)

class AddExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        regions = Region.objects.all()
        branches = Branch.objects.all()
        cost_centers = CostCenter.objects.all()
        heads = Head.objects.all()
        sub_heads = SubHead.objects.all()
        vendors = Vendor.objects.all()
        employees = Employee.objects.all()
        payment_modes = dict(Expense.PAYMENT_MODES)
        
        context = {
            'regions': regions,
            'branches': branches,
            'cost_centers': cost_centers,
            'heads': heads,
            'sub_heads': sub_heads,
            'vendors': vendors,
            'employees': employees,
            'payment_modes': payment_modes,
        }
        
        return render(request, 'expenses/add_expense.html', context)
    
    def post(self, request):
        # This would handle the form submission
        # For now, just redirect back to the expense list
        return redirect('expense_list')

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

# New views for Transaction
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        transactions_list = Transaction.objects.all()
        gl_codes = GLCode.objects.all()
        
        # Filter by GL Code (not implemented yet)
        gl_code_filter = request.GET.get('gl_code')
        
        # Filter by date range (not implemented yet)
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        # Get the show parameter from the request, default to showing all entries
        show = request.GET.get('show', '-1')
        
        # If show is not 'All' (-1), paginate the results
        if show != '-1':
            show = int(show)
            paginator = Paginator(transactions_list, show)
            page = request.GET.get('page', 1)
            transactions = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            # If showing all, no pagination needed
            transactions = transactions_list
            total_pages = 1
        
        context = {
            'transactions': transactions,
            'gl_codes': gl_codes,
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': transactions_list.count()
        }
        return render(request, 'expenses/transaction_list.html', context)

class AddTransactionView(LoginRequiredMixin, View):
    def get(self, request):
        gl_codes = GLCode.objects.all()
        context = {
            'gl_codes': gl_codes
        }
        return render(request, 'expenses/add_transaction.html', context)
    
    def post(self, request):
        # Handle form submission
        gl_code_id = request.POST.get('gl_code')
        date = request.POST.get('date')
        wing_division = request.POST.get('wing_division')
        particulars = request.POST.get('particulars')
        details = request.POST.get('details')
        bill_amount = request.POST.get('bill_amount')
        utilized_limit = request.POST.get('utilized_limit')
        remaining_limit = request.POST.get('remaining_limit')
        
        gl_code = GLCode.objects.get(gl_code=gl_code_id)
        
        Transaction.objects.create(
            gl_code=gl_code,
            date=date,
            wing_division=wing_division,
            particulars=particulars,
            details=details,
            bill_amount=bill_amount,
            utilized_limit=utilized_limit,
            remaining_limit=remaining_limit
        )
        
        return redirect('transaction_list')

class EditTransactionView(LoginRequiredMixin, View):
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return redirect('transaction_list')
        
        gl_codes = GLCode.objects.all()
        context = {
            'transaction': transaction,
            'gl_codes': gl_codes
        }
        
        return render(request, 'expenses/edit_transaction.html', context)
    
    def post(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return redirect('transaction_list')
        
        # Handle form submission
        gl_code_id = request.POST.get('gl_code')
        date = request.POST.get('date')
        wing_division = request.POST.get('wing_division')
        particulars = request.POST.get('particulars')
        details = request.POST.get('details')
        bill_amount = request.POST.get('bill_amount')
        utilized_limit = request.POST.get('utilized_limit')
        remaining_limit = request.POST.get('remaining_limit')
        
        gl_code = GLCode.objects.get(gl_code=gl_code_id)
        
        transaction.gl_code = gl_code
        transaction.date = date
        transaction.wing_division = wing_division
        transaction.particulars = particulars
        transaction.details = details
        transaction.bill_amount = bill_amount
        transaction.utilized_limit = utilized_limit
        transaction.remaining_limit = remaining_limit
        
        transaction.save()
        
        return redirect('transaction_list')

# New views for Vendor
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