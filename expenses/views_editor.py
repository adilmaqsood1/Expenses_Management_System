from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
import json
import datetime

from .models import Vendor, Employee, Expense
from .models_user import AllowanceRequest, User
from django.utils.timezone import now
import datetime

# Custom decorator for editor role check
def editor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_supervisor:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

class EditorRequiredMixin:
    """Mixin to ensure only editors can access the view"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_supervisor:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class EditorDashboardView(LoginRequiredMixin, EditorRequiredMixin, View):
    """Dashboard view for editors"""
    def get(self, request):
        # Get pending allowance requests count
        pending_allowances = AllowanceRequest.objects.filter(status='PENDING').count()
        
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
        recent_allowances = AllowanceRequest.objects.filter(
            processed_by=request.user
        ).order_by('-processed_date')[:5]
        
        allowance_activities = [{
            'type': 'allowance',
            'title': f"Allowance Request {allowance.id}",
            'description': f"Processed for {allowance.user.username} on {allowance.processed_date.strftime('%B %d, %Y')}",
            'amount': allowance.amount,
            'date': allowance.processed_date,
            'status': allowance.status
        } for allowance in recent_allowances]
        
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
        all_activities = allowance_activities + employee_activities + vendor_activities
        recent_activities = sorted(all_activities, key=lambda x: x['date'], reverse=True)[:5]
        
        context = {
            'pending_allowances': pending_allowances,
            'pending_expenses': pending_expenses,
            'employee_count': employee_count,
            'vendor_count': vendor_count,
            'recent_processed': recent_processed,
            'recent_activities': recent_activities
        }
        
        return render(request, 'expenses/editor_dashboard.html', context)

class AllowanceRequestProcessView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for processing allowance requests with approval/rejection reasons"""
    def get(self, request, request_id):
        allowance_request = get_object_or_404(AllowanceRequest, id=request_id)
        
        context = {
            'allowance_request': allowance_request
        }
        return render(request, 'expenses/process_allowance_request.html', context)
    
    def post(self, request, request_id):
        allowance_request = get_object_or_404(AllowanceRequest, id=request_id)
        
        # Process the request
        action = request.POST.get('action')
        if action == 'approve':
            allowance_request.status = 'APPROVED'
            approval_reason = request.POST.get('approval_reason', '')
            allowance_request.approval_reason = approval_reason
            messages.success(request, "Allowance request approved successfully.")
        elif action == 'reject':
            allowance_request.status = 'REJECTED'
            rejection_reason = request.POST.get('rejection_reason', '')
            if not rejection_reason:
                messages.error(request, "Please provide a reason for rejection.")
                return redirect('process_allowance_request', request_id=request_id)
            allowance_request.rejection_reason = rejection_reason
            messages.success(request, "Allowance request rejected successfully.")
        
        # Update processed information
        allowance_request.processed_date = timezone.now()
        allowance_request.processed_by = request.user
        allowance_request.save()
        
        return redirect('editor_allowance_list')

class EditorAllowanceListView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for listing allowance requests for editors"""
    def get(self, request):
        # Get filters from request
        status_filter = request.GET.get('status', 'PENDING')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        # Base queryset
        allowance_requests = AllowanceRequest.objects.all().order_by('-requested_date')
        
        # Apply filters
        if status_filter and status_filter != 'all':
            allowance_requests = allowance_requests.filter(status=status_filter)
        
        if date_from:
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
            allowance_requests = allowance_requests.filter(requested_date__date__gte=date_from)
        
        if date_to:
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
            allowance_requests = allowance_requests.filter(requested_date__date__lte=date_to)
        
        # Pagination
        paginator = Paginator(allowance_requests, 10)
        page = request.GET.get('page', 1)
        allowance_requests = paginator.get_page(page)
        
        context = {
            'allowance_requests': allowance_requests,
            'status_filter': status_filter,
            'date_from': date_from.strftime('%Y-%m-%d') if date_from else '',
            'date_to': date_to.strftime('%Y-%m-%d') if date_to else ''
        }
        
        return render(request, 'expenses/editor_allowance_list.html', context)

class EditorEmployeeListView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for listing employees for editors"""
    def get(self, request):
        employees_list = Employee.objects.all()
        
        # Apply filters
        name_filter = request.GET.get('name')
        if name_filter:
            employees_list = employees_list.filter(name__icontains=name_filter)
            
        designation_filter = request.GET.get('designation')
        if designation_filter:
            employees_list = employees_list.filter(designation__icontains=designation_filter)
        
        # Pagination
        show = request.GET.get('show', '10')
        if show != '-1':
            show = int(show)
            paginator = Paginator(employees_list, show)
            page = request.GET.get('page', 1)
            employees = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
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
        
        return render(request, 'expenses/editor_employee_list.html', context)

class EditorAddEmployeeView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for adding a new employee by editors"""
    def get(self, request):
        return render(request, 'expenses/editor_add_employee.html')
    
    def post(self, request):
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        sap_id = request.POST.get('sap_id')
        account = request.POST.get('account')
        account_type = request.POST.get('account_type')
        account_name = request.POST.get('account_name')
        account_number = request.POST.get('account_number')
        
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
            account_name=account_name,
            account_number=account_number
        )
        employee.save()
        
        messages.success(request, f"Employee {name} added successfully.")
        return redirect('editor_employee_list')

class EditorEditEmployeeView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for editing an existing employee by editors"""
    def get(self, request, employee_id):
        employee = get_object_or_404(Employee, sap_id=employee_id)
        
        context = {
            'employee': employee
        }
        
        return render(request, 'expenses/editor_edit_employee.html', context)
    
    def post(self, request, employee_id):
        employee = get_object_or_404(Employee, sap_id=employee_id)
        
        employee.name = request.POST.get('name')
        employee.designation = request.POST.get('designation')
        employee.address = request.POST.get('address')
        employee.email = request.POST.get('email')
        employee.phone_no = request.POST.get('phone_no')
        employee.account = request.POST.get('account')
        employee.account_type = request.POST.get('account_type')
        employee.account_name = request.POST.get('account_name')
        employee.account_number = request.POST.get('account_number')
        
        employee.save()
        
        messages.success(request, f"Employee {employee.name} updated successfully.")
        return redirect('editor_employee_list')

class EditorVendorListView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for listing vendors for editors"""
    def get(self, request):
        vendors_list = Vendor.objects.all()
        
        # Apply filters
        name_filter = request.GET.get('name')
        if name_filter:
            vendors_list = vendors_list.filter(name__icontains=name_filter)
            
        type_filter = request.GET.get('type')
        if type_filter:
            vendors_list = vendors_list.filter(type=type_filter)
            
        status_filter = request.GET.get('status')
        if status_filter:
            if status_filter == 'Active':
                vendors_list = vendors_list.filter(disabled=False)
            elif status_filter == 'Inactive':
                vendors_list = vendors_list.filter(disabled=True)
        
        # Pagination
        show = request.GET.get('show', '10')
        if show != '-1':
            show = int(show)
            paginator = Paginator(vendors_list, show)
            page = request.GET.get('page', 1)
            vendors = paginator.get_page(page)
            total_pages = paginator.num_pages
        else:
            vendors = vendors_list
            total_pages = 1
        
        context = {
            'vendors': vendors,
            'selected_name': name_filter or '',
            'selected_type': type_filter or '',
            'selected_status': status_filter or '',
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': vendors_list.count()
        }
        
        return render(request, 'expenses/editor_vendor_list.html', context)

class EditorAddVendorView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for adding a new vendor by editors"""
    def get(self, request):
        return render(request, 'expenses/editor_add_vendor.html')
    
    def post(self, request):
        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        type = request.POST.get('type')
        status = request.POST.get('status', 'Active')
        
        # Create new vendor
        vendor = Vendor(
            name=name,
            cnic=cnic,
            type=type,
            status=status,
            disabled=False
        )
        vendor.save()
        
        messages.success(request, f"Vendor {name} added successfully.")
        return redirect('editor_vendor_list')

class EditorEditVendorView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for editing an existing vendor by editors"""
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        context = {
            'vendor': vendor
        }
        
        return render(request, 'expenses/editor_edit_vendor.html', context)
    
    def post(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        vendor.name = request.POST.get('name')
        vendor.cnic = request.POST.get('cnic')
        vendor.type = request.POST.get('type')
        vendor.status = request.POST.get('status')
        vendor.disabled = request.POST.get('status') == 'Inactive'
        
        vendor.save()
        
        messages.success(request, f"Vendor {vendor.name} updated successfully.")
        return redirect('editor_vendor_list')

class EditorToggleVendorStatusView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for toggling vendor status (active/inactive)"""
    def post(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        # Toggle disabled status
        vendor.disabled = not vendor.disabled
        vendor.status = 'Inactive' if vendor.disabled else 'Active'
        vendor.save()
        
        status_text = 'deactivated' if vendor.disabled else 'activated'
        messages.success(request, f"Vendor {vendor.name} {status_text} successfully.")
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'vendor_status': 'Inactive' if vendor.disabled else 'Active'
            })
        
        return redirect('editor_vendor_list')

class EditorExpenseListView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for listing expenses for editors to approve or reject"""
    def get(self, request):
        expenses_list = Expense.objects.all().order_by('-created_date')
        vendors = Vendor.objects.all()
        employees = Employee.objects.all()
        status_choices = dict(Expense.STATUS_CHOICES)
        expense_types = ['Vendor', 'Employee']
        
        # Filter based on user role
        if request.user.is_supervisor and not request.user.is_admin:
            # Supervisors see pending expenses or ones they've already processed
            expenses_list = expenses_list.filter(
                Q(supervisor_approval='Pending') | 
                Q(supervisor=request.user)
            )
        elif request.user.is_admin:
            # Admins see expenses approved by supervisors but pending admin approval,
            # or ones they've already processed
            expenses_list = expenses_list.filter(
                Q(supervisor_approval='Approved', admin_approval='Pending') | 
                Q(admin=request.user)
            )
            
        # Apply filters
        # Date filters
        start_date = request.GET.get('start_date')
        if start_date:
            expenses_list = expenses_list.filter(created_date__gte=start_date)
            
        end_date = request.GET.get('end_date')
        if end_date:
            expenses_list = expenses_list.filter(created_date__lte=end_date)
        
        # Type filter
        type_filter = request.GET.get('type')
        
        # Vendor filter
        vendor_filter = request.GET.get('vendor')
        if vendor_filter:
            expenses_list = expenses_list.filter(vendor_id=vendor_filter)
        
        # Employee filter (not implemented yet as it's not a field in Expense model)
        employee_filter = request.GET.get('employee')
        
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
        
        # Count expenses processed today
        today = now().date()
        processed_today = Expense.objects.filter(
            Q(status='Approved') | Q(status='Rejected'),
            created_date=today
        ).count()
        
        context = {
            'expenses': expenses,
            'vendors': vendors,
            'employees': employees,
            'status_choices': status_choices,
            'expense_types': expense_types,
            'show': show,
            'total_pages': total_pages,
            'current_page': int(request.GET.get('page', 1)),
            'total_count': expenses_list.count(),
            'processed_today': processed_today,
            'start_date': start_date,
            'end_date': end_date
        }
        
        return render(request, 'expenses/editor_expense_list.html', context)

class ProcessExpenseView(LoginRequiredMixin, EditorRequiredMixin, View):
    """View for processing expense requests with approval/rejection reasons"""
    def get(self, request, expense_id=None):
        # If expense_id is provided, show the individual expense processing page
        if expense_id:
            expense = get_object_or_404(Expense, id=expense_id)
            context = {
                'expense': expense,
                'is_admin': request.user.is_admin
            }
            return render(request, 'expenses/process_expense.html', context)
        
        # If no expense_id, redirect to the expense list
        return redirect('editor_expense_list')
    
    def post(self, request, expense_id=None):
        # Handle form submission from the expense list page
        if not expense_id:
            expense_id = request.POST.get('expense_id')
            if not expense_id:
                messages.error(request, "No expense specified.")
                return redirect('editor_expense_list')
        
        expense = get_object_or_404(Expense, id=expense_id)
        
        # Process the expense based on user role
        action = request.POST.get('action')
        
        # Admin approval process
        if request.user.is_admin:
            # Check if supervisor has already approved
            if expense.supervisor_approval != 'Approved':
                messages.warning(request, "This expense must be approved by a supervisor first.")
                return redirect('editor_expense_list')
                
            if action == 'approve':
                expense.admin_approval = 'Approved'
                expense.status = 'Approved'  # Final status is set to Approved
                expense.admin_remarks = request.POST.get('approval_reason', '')
                expense.admin = request.user
                expense.admin_date = timezone.now()
                messages.success(request, "Expense approved successfully.")
            elif action == 'reject':
                expense.admin_approval = 'Rejected'
                expense.status = 'Rejected'  # Final status is set to Rejected
                rejection_reason = request.POST.get('rejection_reason', '')
                if not rejection_reason:
                    messages.error(request, "Please provide a reason for rejection.")
                    return redirect('process_expense', expense_id=expense_id)
                expense.admin_remarks = rejection_reason
                expense.admin = request.user
                expense.admin_date = timezone.now()
                messages.success(request, "Expense rejected successfully.")
        
        # Supervisor approval process
        elif request.user.is_supervisor:
            if action == 'approve':
                expense.supervisor_approval = 'Approved'
                expense.supervisor_remarks = request.POST.get('approval_reason', '')
                expense.supervisor = request.user
                expense.supervisor_date = timezone.now()
                # Status remains Pending until admin approves
                messages.success(request, "Expense approved by supervisor. Awaiting admin approval.")
            elif action == 'reject':
                expense.supervisor_approval = 'Rejected'
                expense.status = 'Rejected'  # If supervisor rejects, final status is Rejected
                rejection_reason = request.POST.get('rejection_reason', '')
                if not rejection_reason:
                    messages.error(request, "Please provide a reason for rejection.")
                    return redirect('process_expense', expense_id=expense_id)
                expense.supervisor_remarks = rejection_reason
                expense.supervisor = request.user
                expense.supervisor_date = timezone.now()
                messages.success(request, "Expense rejected by supervisor.")
        else:
            messages.error(request, "You don't have permission to process expenses.")
            return redirect('dashboard')
        
        # Save the expense
        expense.save()
        
        return redirect('editor_expense_list')