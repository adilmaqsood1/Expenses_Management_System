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
            # If branch code is stored in the Branch model and related to user somehow
            # For this example, we're assuming branch code is the first Branch object
            # In a real application, you would have a proper relationship between User and Branch
            branch = Branch.objects.first()
            if branch:
                context['branch_code'] = branch.code
            else:
                context['branch_code'] = 'N/A'
        except Exception:
            context['branch_code'] = 'N/A'
    
    return context