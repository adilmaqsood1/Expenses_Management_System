from django.conf import settings

def user_context(request):
    """
    Context processor to add user information to all templates.
    This makes the current user's username available in all templates.
    """
    context = {}
    
    # Add username to context if user is authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['branch_code'] = 'N/A'
        context['branch_name'] = 'No Branch'
    else:
        context['branch_code'] = 'N/A'
    
    return context

def user_info(request):
    """
    Context processor to add user information to all templates.
    This provides user role and other information to templates.
    """
    context = {}
    
    # Add user information to context if user is authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['user_role'] = getattr(request.user, 'role', 'Unknown')
        context['is_admin'] = getattr(request.user, 'is_admin', False)
        context['is_editor'] = getattr(request.user, 'is_editor', False)
        context['is_mis'] = getattr(request.user, 'is_mis', False)
        context['is_subhead'] = getattr(request.user, 'is_subhead', False)
        context['branch_code'] = 'N/A'
        context['branch_name'] = 'No Branch'
    else:
        context['branch_code'] = 'N/A'
        context['user_role'] = 'Anonymous'
    
    return context