from django.urls import path
from . import views, api, views_mis, views_editor
from django.contrib.auth import views as auth_views

app_name = 'budget'

from .views import SupervisorStationaryRequestsView

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('admin-login/', auth_views.LoginView.as_view(template_name='admin/login.html', next_page='/admin/'), name='admin_login'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/detail/<int:expense_id>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/add/', views.AddExpenseView.as_view(), name='add_expense'),
    path('expenditure_claim/<int:expense_id>/', views.expenditure_claim_view, name='expenditure_claim'), # New URL for expenditure claim
    path('gl-codes/', views.GLCodeListView.as_view(), name='gl_code_list'),
    path('gl-codes/add/', views.AddGLCodeView.as_view(), name='add_gl_code'),
    path('gl-codes/edit/<str:gl_code_id>/', views.EditGLCodeView.as_view(), name='edit_gl_code'),
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add/', views.AddVendorView.as_view(), name='add_vendor'),
    path('vendors/edit/<int:vendor_id>/', views.EditVendorView.as_view(), name='edit_vendor'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('employees/edit/<str:employee_id>/', views.EditEmployeeView.as_view(), name='edit_employee'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # API endpoints
    path('api/head-budget/<int:head_id>/', api.head_budget, name='api_head_budget'),
    # path('api/subhead-budget/<int:subhead_id>/', api_budget.subhead_budget, name='api_subhead_budget'),
    path('api/mis-dashboard-data/', views_mis.MISDashboardDataAPIView.as_view(), name='api_mis_dashboard_data'),
    
    # MIS Dashboard
    path('mis-dashboard/', views_mis.MISDashboardView.as_view(), name='mis_dashboard'),
    
    # Editor views
    path('editor/expenses/', views_editor.EditorExpenseListView.as_view(), name='editor_expense_list'),
    path('editor/expenses/process/', views_editor.ProcessExpenseView.as_view(), name='process_expense'),
    path('editor/expenses/process/<int:expense_id>/', views_editor.ProcessExpenseView.as_view(), name='process_expense'),
    
    # Stationary Requests
    path('stationary-request/', views.StationaryRequestView.as_view(), name='stationary_request'),
    path('supervisor-stationary-requests/', SupervisorStationaryRequestsView.as_view(), name='supervisor_stationary_requests'),
    path('stationary-requests-list/', views.stationary_request_userlist, name='stationary_requests_userlist'),
]