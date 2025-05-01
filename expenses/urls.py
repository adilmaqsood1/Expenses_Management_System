from django.urls import path
from . import views, api, views_allowance, views_mis, views_editor

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/detail/<int:expense_id>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/add/', views.AddExpenseView.as_view(), name='add_expense'),
    path('expenditure_claim/<int:expense_id>/', views.expenditure_claim_view, name='expenditure_claim'), # New URL for expenditure claim
    path('gl-codes/', views.GLCodeListView.as_view(), name='gl_code_list'),
    path('gl-codes/add/', views.AddGLCodeView.as_view(), name='add_gl_code'),
    path('gl-codes/edit/<str:gl_code_id>/', views.EditGLCodeView.as_view(), name='edit_gl_code'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('transactions/edit/<int:transaction_id>/', views.EditTransactionView.as_view(), name='edit_transaction'),
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add/', views.AddVendorView.as_view(), name='add_vendor'),
    path('vendors/edit/<int:vendor_id>/', views.EditVendorView.as_view(), name='edit_vendor'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('employees/edit/<str:employee_id>/', views.EditEmployeeView.as_view(), name='edit_employee'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Allowance request URLs
    path('allowance-requests/', views_allowance.AllowanceRequestListView.as_view(), name='allowance_request_list'),
    path('allowance-requests/create/', views_allowance.CreateAllowanceRequestView.as_view(), name='create_allowance_request'),
    path('allowance-requests/detail/<int:request_id>/', views_allowance.AllowanceRequestDetailView.as_view(), name='allowance_request_detail'),
    path('allowance-requests/process/<int:request_id>/', views_allowance.ProcessAllowanceRequestView.as_view(), name='process_allowance_request'),
    path('allowance-requests/analytics/', views_allowance.AllowanceAnalyticsView.as_view(), name='allowance_analytics'),
    
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
    path('editor/allowances/', views_editor.EditorAllowanceListView.as_view(), name='editor_allowance_list'),
    path('editor/allowances/process/<int:request_id>/', views_editor.AllowanceRequestProcessView.as_view(), name='process_allowance_request'),
]