from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from decimal import Decimal
import json
import datetime

from .models import Expense, Head, Vendor, Region
from .models_user import User

class MISDashboardView(LoginRequiredMixin, View):
    """
    View for the MIS Analytics Dashboard
    Only accessible to users with the MIS role
    """
    def get(self, request):
        # Check if user has MIS role
        if not request.user.is_mis:
            # Redirect non-MIS users to the regular dashboard
            return redirect('dashboard')
        
        # Get all data needed for the dashboard
        context = self.get_dashboard_data()
        return render(request, 'expenses/mis_dashboard.html', context)
    
    def get_dashboard_data(self, filters=None):
        """
        Get all data needed for the dashboard
        If filters are provided, apply them to the data
        """
        # Default filter is last 30 days
        end_date = timezone.now().date()
        start_date = end_date - datetime.timedelta(days=30)
        
        # Apply filters if provided
        if filters:
            date_range = filters.get('date_range')
            if date_range == 'custom':
                start_date = datetime.datetime.strptime(filters.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(filters.get('end_date'), '%Y-%m-%d').date()
            elif date_range == '7':
                start_date = end_date - datetime.timedelta(days=7)
            elif date_range == '90':
                start_date = end_date - datetime.timedelta(days=90)
            elif date_range == '365':
                start_date = end_date - datetime.timedelta(days=365)
            
            # Filter by head
            head_filter = filters.get('head')
            vendor_filter = filters.get('vendor')
            status_filter = filters.get('status')
        
        # Base queryset with date filter
        expenses = Expense.objects.filter(created_date__gte=start_date, created_date__lte=end_date)
        
        # Apply additional filters if provided
        if filters:
            if head_filter and head_filter != 'all':
                expenses = expenses.filter(gl_code_id=head_filter)
            if vendor_filter and vendor_filter != 'all':
                expenses = expenses.filter(vendor_id=vendor_filter)
            if status_filter and status_filter != 'all':
                expenses = expenses.filter(status=status_filter)
        
        # Get summary statistics
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        expense_count = expenses.count()
        approved_count = expenses.filter(status='Approved').count()
        pending_count = expenses.filter(status='Pending').count()
        avg_expense = expenses.aggregate(Avg('amount'))['amount__avg'] or 0
        
        # Calculate budget utilization
        total_budget = Head.objects.aggregate(Sum('budget'))['budget__sum'] or Decimal('1')
        utilized_budget = expenses.filter(status='Approved').aggregate(Sum('amount'))['amount__sum'] or 0
        budget_utilization = int((utilized_budget / total_budget) * 100) if total_budget > 0 else 0
        
        # Get expense by head data
        expenses_by_head = expenses.values('gl_code__gl_description').annotate(total=Sum('amount')).order_by('-total')
        head_labels = [item['gl_code__gl_description'] for item in expenses_by_head]
        head_values = [float(item['total']) for item in expenses_by_head]
        
        # Get expense trend data (last 12 months)
        trend_data = []
        trend_labels = []
        
        for i in range(11, -1, -1):
            month_date = end_date - datetime.timedelta(days=30 * i)
            month_name = month_date.strftime('%b %Y')
            month_expenses = expenses.filter(
                created_date__month=month_date.month,
                created_date__year=month_date.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            trend_labels.append(month_name)
            trend_data.append(float(month_expenses))
        

        
        # Get expense by status data
        expenses_by_status = expenses.values('status').annotate(total=Sum('amount')).order_by('status')
        status_labels = [item['status'] for item in expenses_by_status]
        status_values = [float(item['total']) for item in expenses_by_status]
        
        # Region data has been removed
        region_labels = []
        region_values = []
        
        # Get top vendors data
        top_vendors = expenses.values('vendor__name').annotate(total=Sum('amount')).order_by('-total')[:5]
        vendor_labels = [item['vendor__name'] for item in top_vendors]
        vendor_values = [float(item['total']) for item in top_vendors]
        
        # Get monthly comparison data (current year vs previous year)
        current_year = end_date.year
        previous_year = current_year - 1
        
        monthly_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_year_values = []
        previous_year_values = []
        
        for month in range(1, 13):
            # Current year monthly expenses
            current_month_expenses = Expense.objects.filter(
                created_date__month=month,
                created_date__year=current_year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Previous year monthly expenses
            previous_month_expenses = Expense.objects.filter(
                created_date__month=month,
                created_date__year=previous_year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            current_year_values.append(float(current_month_expenses))
            previous_year_values.append(float(previous_month_expenses))
        
        # Get top expenses for table
        top_expenses = expenses.order_by('-amount')[:10]
        
        # Get all heads and vendors for filters
        heads = Head.objects.all()
        vendors = Vendor.objects.all()
        
        # Prepare context
        context = {
            'total_expenses': total_expenses,
            'expense_count': expense_count,
            'approved_count': approved_count,
            'pending_count': pending_count,
            'avg_expense': avg_expense,
            'budget_utilization': budget_utilization,
            'head_labels': json.dumps(head_labels),
            'head_values': json.dumps(head_values),
            'trend_labels': json.dumps(trend_labels),
            'trend_values': json.dumps(trend_data),

            'status_labels': json.dumps(status_labels),
            'status_values': json.dumps(status_values),
            'vendor_labels': json.dumps(vendor_labels),
            'vendor_values': json.dumps(vendor_values),

            'monthly_labels': json.dumps(monthly_labels),
            'current_year_values': json.dumps(current_year_values),
            'previous_year_values': json.dumps(previous_year_values),
            'top_expenses': top_expenses,
            'heads': heads,
            'vendors': vendors,
            'regions': Region.objects.all(),
        }
        
        return context

class MISDashboardDataAPIView(LoginRequiredMixin, View):
    """
    API view for getting filtered dashboard data
    """
    def post(self, request):
        # Check if user has MIS role
        if not request.user.is_mis:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        # Get filters from request
        try:
            filters = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Get dashboard data with filters
        dashboard_view = MISDashboardView()
        context = dashboard_view.get_dashboard_data(filters)
        
        # Prepare response data
        response_data = {
            'summary': {
                'total_expenses': float(context['total_expenses']),
                'expense_count': context['expense_count'],
                'avg_expense': float(context['avg_expense']),
                'budget_utilization': context['budget_utilization']
            },
            'charts': {
                'head_labels': json.loads(context['head_labels']),
                'head_values': json.loads(context['head_values']),
                'trend_labels': json.loads(context['trend_labels']),
                'trend_values': json.loads(context['trend_values']),

                'status_labels': json.loads(context['status_labels']),
                'status_values': json.loads(context['status_values']),
                'vendor_labels': json.loads(context['vendor_labels']),
                'vendor_values': json.loads(context['vendor_values']),

                'monthly_labels': json.loads(context['monthly_labels']),
                'current_year_values': json.loads(context['current_year_values']),
                'previous_year_values': json.loads(context['previous_year_values'])
            },
            'top_expenses': [
                {
                    'invoice_no': expense.invoice_no,
                    'head_name': expense.gl_code.gl_description if expense.gl_code else '',
                    'vendor_name': expense.vendor.name if expense.vendor else '',
                    'invoice_date': expense.invoice_date.isoformat(),
                    'amount': float(expense.amount),
                    'status': expense.status
                } for expense in context['top_expenses']
            ]
        }
        
        return JsonResponse(response_data)