from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Expense, Vendor, GLCode
from .models_user import User

def admin_dashboard_stats(request):
    """
    Context processor to provide statistics for the admin dashboard
    """
    if not request.path.startswith('/admin/'):
        return {}
    
    # Get expense statistics
    expense_count = Expense.objects.count()
    pending_count = Expense.objects.filter(status='Pending').count()
    vendor_count = Vendor.objects.filter(disabled=False).count()
    
    # Calculate budget utilization
    total_budget = GLCode.objects.aggregate(total=Sum('limit'))['total'] or 0
    total_utilized = GLCode.objects.aggregate(total=Sum('limit_utilized'))['total'] or 0
    budget_utilization = f"{(total_utilized / total_budget) * 100:.1f}%" if total_budget > 0 else "0%"
    
    # Get active users
    active_users = User.objects.filter(is_active=True).count()
    
    # Recent activities (last 7 days)
    recent_date = timezone.now() - timedelta(days=7)
    recent_expenses = Expense.objects.filter(created_date__gte=recent_date).order_by('-created_date')[:5]
    
    recent_activities = []
    for expense in recent_expenses:
        activity = {
            'date': expense.created_date.strftime('%b %d, %Y'),
            'time': expense.created_date.strftime('%H:%M'),
            'title': f"Expense {expense.invoice_no}",
            'description': f"{expense.vendor.name} - ${expense.amount}",
            'icon': 'fa-money-bill'
        }
        recent_activities.append(activity)
    
    return {
        'expense_count': expense_count,
        'pending_count': pending_count,
        'vendor_count': vendor_count,
        'budget_utilization': budget_utilization,
        'active_users': active_users,
        'recent_activities': recent_activities
    }