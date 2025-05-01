from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from functools import wraps
from .models_user import AllowanceRequest, User

# Role-based permission decorator
def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('dashboard')
        return _wrapped_view
    return decorator

class AllowanceRequestListView(LoginRequiredMixin, View):
    def get(self, request):
        # Different views based on user role
        if request.user.is_admin:
            # Admins can see all requests
            allowance_requests = AllowanceRequest.objects.all().order_by('-requested_date')
        elif request.user.is_supervisor:
            # Editors see pending requests they need to process
            allowance_requests = AllowanceRequest.objects.filter(status='PENDING').order_by('-requested_date')
        elif request.user.is_mis:
            # MIS users can see all requests for analysis
            allowance_requests = AllowanceRequest.objects.all().order_by('-requested_date')
        else:
            # Regular users (sub-heads) only see their own requests
            allowance_requests = AllowanceRequest.objects.filter(user=request.user).order_by('-requested_date')
        
        context = {
            'allowance_requests': allowance_requests,
            'user_role': request.user.role
        }
        return render(request, 'expenses/allowance_request_list.html', context)

class CreateAllowanceRequestView(LoginRequiredMixin, View):
    def get(self, request):
        # Only sub-heads (USER role) can create allowance requests
        if not request.user.is_maker:
            messages.error(request, "You don't have permission to create allowance requests.")
            return redirect('dashboard')
        
        return render(request, 'expenses/create_allowance_request.html')
    
    def post(self, request):
        if not request.user.is_supervisor:
            messages.error(request, "You don't have permission to create allowance requests.")
            return redirect('dashboard')
        
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose')
        
        # Create new allowance request
        AllowanceRequest.objects.create(
            user=request.user,
            amount=amount,
            purpose=purpose,
            status='PENDING'
        )
        
        messages.success(request, "Allowance request submitted successfully.")
        return redirect('allowance_request_list')

class ProcessAllowanceRequestView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        # Only editors and admins can process requests
        if not (request.user.is_editor or request.user.is_admin):
            messages.error(request, "You don't have permission to process allowance requests.")
            return redirect('dashboard')
        
        allowance_request = get_object_or_404(AllowanceRequest, id=request_id)
        
        context = {
            'allowance_request': allowance_request
        }
        return render(request, 'expenses/process_allowance_request.html', context)
    
    def post(self, request, request_id):
        if not (request.user.is_editor or request.user.is_admin):
            messages.error(request, "You don't have permission to process allowance requests.")
            return redirect('dashboard')
        
        allowance_request = get_object_or_404(AllowanceRequest, id=request_id)
        
        # Process the request
        action = request.POST.get('action')
        if action == 'approve':
            allowance_request.status = 'APPROVED'
            messages.success(request, "Allowance request approved successfully.")
        elif action == 'reject':
            allowance_request.status = 'REJECTED'
            allowance_request.rejection_reason = request.POST.get('rejection_reason')
            messages.success(request, "Allowance request rejected.")
        
        allowance_request.processed_date = timezone.now()
        allowance_request.processed_by = request.user
        allowance_request.save()
        
        return redirect('allowance_request_list')

class AllowanceRequestDetailView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        # Get the allowance request
        allowance_request = get_object_or_404(AllowanceRequest, id=request_id)
        
        # Check if the user has permission to view this request
        if not (request.user.is_admin or request.user.is_editor or request.user.is_mis or request.user == allowance_request.user):
            messages.error(request, "You don't have permission to view this allowance request.")
            return redirect('dashboard')
        
        context = {
            'allowance_request': allowance_request
        }
        return render(request, 'expenses/allowance_request_detail.html', context)

class AllowanceAnalyticsView(LoginRequiredMixin, View):
    def get(self, request):
        # Only MIS and admin users can access analytics
        if not (request.user.is_mis or request.user.is_admin):
            messages.error(request, "You don't have permission to view allowance analytics.")
            return redirect('dashboard')
        
        # Get all users with USER role (sub-heads)
        subheads = User.objects.filter(role='MAKERS')
        
        # Analytics data
        analytics = []
        for subhead in subheads:
            total_requests = AllowanceRequest.objects.filter(user=subhead).count()
            approved_requests = AllowanceRequest.objects.filter(user=subhead, status='APPROVED').count()
            rejected_requests = AllowanceRequest.objects.filter(user=subhead, status='REJECTED').count()
            total_amount = sum(req.amount for req in AllowanceRequest.objects.filter(user=subhead, status='APPROVED'))
            
            analytics.append({
                'user': subhead,
                'total_requests': total_requests,
                'approved_requests': approved_requests,
                'rejected_requests': rejected_requests,
                'total_amount': total_amount,
                # Remove reference to branch which no longer exists
                # 'branch': subhead.branch
            })
        
        context = {
            'analytics': analytics
        }
        return render(request, 'expenses/allowance_analytics.html', context)