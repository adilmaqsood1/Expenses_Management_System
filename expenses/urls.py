from django.urls import path
from . import views, api, views_allowance

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.AddExpenseView.as_view(), name='add_expense'),
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
    path('allowance-requests/process/<int:request_id>/', views_allowance.ProcessAllowanceRequestView.as_view(), name='process_allowance_request'),
    path('allowance-requests/analytics/', views_allowance.AllowanceAnalyticsView.as_view(), name='allowance_analytics'),
    
    # API endpoints
    path('api/head-budget/<int:head_id>/', api.head_budget, name='api_head_budget'),
]