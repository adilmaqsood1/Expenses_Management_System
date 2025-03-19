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

class CustomLoginView(LoginView):
    template_name = 'expenses/login.html'
    redirect_field_name = 'next'
    next_page = 'dashboard' 
    
class RegisterView(View):
    template_name = 'expenses/register.html'

    def get(self, request):
        return render(request, self.template_name) 



class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        # Get total expenses
        total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Get pending approvals count
        pending_approvals = Expense.objects.filter(status='Pending').count()
        
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
        all_activities = expense_activities + transaction_activities + vendor_activities
        recent_activities = sorted(all_activities, key=lambda x: x['date'], reverse=True)[:5]
        
        context = {
            'total_expenses': total_expenses,
            'pending_approvals': pending_approvals,
            'budget_utilization': budget_utilization,
            'month_change_percentage': month_change_percentage,
            'month_change_direction': 'up' if month_change_percentage >= 0 else 'down',
            'recent_activities': recent_activities
        }
        
        return render(request, 'expenses/dashboard.html', context)

class ExpenseListView(LoginRequiredMixin, View):
    def get(self, request):
        expenses = Expense.objects.all()
        context = {
            'expenses': expenses
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
        
        context = {
            'regions': regions,
            'branches': branches,
            'cost_centers': cost_centers,
            'heads': heads,
            'sub_heads': sub_heads,
            'vendors': vendors,
        }
        
        return render(request, 'expenses/add_expense.html', context)
    
    def post(self, request):
        # This would handle the form submission
        # For now, just redirect back to the expense list
        return redirect('expense_list')

# New views for GLCode
class GLCodeListView(LoginRequiredMixin, View):
    def get(self, request):
        gl_codes = GLCode.objects.all()
        context = {
            'gl_codes': gl_codes
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
        
        GLCode.objects.create(
            gl_code=gl_code,
            gl_description=gl_description,
            limit_in_millions=limit_in_millions if limit_in_millions else None,
            limit=limit if limit else None
        )
        
        return redirect('gl_code_list')

# New views for Transaction
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = Transaction.objects.all()
        context = {
            'transactions': transactions
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

# New views for Vendor
class VendorListView(LoginRequiredMixin, View):
    def get(self, request):
        vendors = Vendor.objects.all()
        context = {
            'vendors': vendors
        }
        return render(request, 'expenses/vendor_list.html', context)

class AddVendorView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'expenses/add_vendor.html')
    
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