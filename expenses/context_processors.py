from django.contrib.auth import get_user_model
from .models import Branch

def user_info(request):
    """
    Context processor to add user information to all templates.
    This makes the current user's username and branch code available in all templates.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Get the username from the authenticated user
        username = request.user.username
        context['username'] = username
        
        # Try to get branch code - assuming branch code might be in the username
        # For example, if username format is like 'ft.branch2', extract '2' as branch code
        # This is just an example, adjust according to your actual username format
        try:
            # Get the user's branch if it exists
            if hasattr(request.user, 'branch') and request.user.branch:
                context['branch_code'] = request.user.branch.code
                context['branch_name'] = request.user.branch.name
            else:
                context['branch_code'] = 'N/A'
                context['branch_name'] = 'No Branch'
        except Exception:
            context['branch_code'] = 'N/A'
    
    return context