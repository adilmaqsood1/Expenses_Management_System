# Expense Management System

A comprehensive web application for managing organizational expenses, budgets, and financial transactions.

## Overview

The Expense Management System is a Django-based application designed to help organizations track and manage their expenses efficiently. It provides features for expense posting, budget tracking, vendor management, and financial reporting.

## Features

- **Expense Tracking**: Record and categorize expenses with detailed information
- **Budget Management**: Track budget utilization across different heads and departments
- **Vendor Management**: Maintain a database of vendors and their details
- **Financial Reporting**: Generate reports on expenses and budget utilization
- **User Authentication**: Secure login and user management system
- **Dashboard**: Visual representation of financial data and recent activities
- **Transaction Management**: Record and track financial transactions

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (Neon DB)
- **Frontend**: HTML, CSS, JavaScript
- **Additional Libraries**:
  - django-crispy-forms & crispy-bootstrap4 for form styling
  - django-import-export for data import/export functionality
  - whitenoise for static file serving
  - gunicorn as the WSGI HTTP server

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL (or use the configured Neon DB)
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd expense_management
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database:
   - The project is configured to use Neon DB (PostgreSQL)
   - You can modify the database settings in `expense_management/settings.py` if needed

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://localhost:8000

## Project Structure

- **expense_management/**: Main project settings and configuration
- **expenses/**: Main application with models, views, and business logic
- **templates/**: HTML templates for the application
- **static/**: Static files (CSS, JavaScript, images)
- **staticfiles/**: Collected static files for production

## Data Models

- **Region**: Geographic regions for organizational structure
- **Branch**: Branches within regions
- **CostCenter**: Cost centers for expense allocation
- **Head**: Budget heads for categorizing expenses
- **SubHead**: Sub-categories under budget heads
- **Vendor**: Vendor/supplier information
- **Expense**: Expense records with detailed information
- **Transaction**: Financial transaction records
- **GLCode**: General Ledger codes for accounting

## Usage

1. **Login**: Access the system using your credentials
2. **Dashboard**: View financial overview and recent activities
3. **Add Expense**: Record new expenses with invoice details
4. **Manage Vendors**: Add and manage vendor information
5. **View Reports**: Access financial reports and budget utilization

## Deployment

The application is configured for deployment on Vercel with the included `vercel.json` configuration file.

## License

[Specify License]

## Contributors

[List Contributors]