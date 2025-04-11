from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .models import Head, Expense, GLCode
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

@require_GET
@login_required
def head_budget(request, head_id):
    """
    API endpoint to get budget information for a specific head
    """
    try:
        # Get the head object
        head = Head.objects.get(code=head_id)
        
        # Get total budget for this head
        total_budget = head.budget
        
        # Calculate utilized budget (sum of approved expenses for this head)
        utilized_budget = Expense.objects.filter(
            # head=head,
            status='Approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        # Calculate available budget
        available_budget = total_budget - utilized_budget
        
        # Calculate monthly financial limit (simplified example)
        # In a real application, this might be based on business rules
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_expenses = Expense.objects.filter(
            # head=head,
            created_date__month=current_month,
            created_date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        # For this example, we'll set monthly limit as 1/12 of the total budget
        monthly_limit = total_budget / 12
        
        # Return the budget information as JSON
        return JsonResponse({
            'total_budget': float(total_budget),
            'utilized_budget': float(utilized_budget),
            'available_budget': float(available_budget),
            'monthly_limit': float(monthly_limit),
            'monthly_expenses': float(monthly_expenses)
        })
        
    except Head.DoesNotExist:
        return JsonResponse({'error': 'Head not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)