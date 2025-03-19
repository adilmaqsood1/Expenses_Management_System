from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.AddExpenseView.as_view(), name='add_expense'),
    path('gl-codes/', views.GLCodeListView.as_view(), name='gl_code_list'),
    path('gl-codes/add/', views.AddGLCodeView.as_view(), name='add_gl_code'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/add/', views.AddVendorView.as_view(), name='add_vendor'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # API endpoints
    path('api/head-budget/<int:head_id>/', api.head_budget, name='api_head_budget'),
]