"""
URL configuration for expense_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'expense'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='expenses/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='expenses/password_change_done.html'), name='password_change_done'),
    path('logouts/', auth_views.LogoutView.as_view(next_page='budget:login'), name='logouts'),
]
