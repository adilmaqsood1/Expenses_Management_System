"""
Django settings for expense_management project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# import dj_database_url
import cloudinary
import dotenv
dotenv.load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "True"
# DEBUG = True

ALLOWED_HOSTS = ['*','.vercel.app', os.getenv("ALLOW_HOST", " localhost")]




# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Add Jazzmin before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', 
    'expenses.apps.ExpensesConfig',
    'import_export',
    
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

if os.getenv("DATABASE_URL"):
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expense_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'expenses.context_processors.user_info',
                'expenses.admin_context_processors.admin_dashboard_stats',
            ],
        },
    },
]

WSGI_APPLICATION = 'expense_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if os.getenv("DATABASE_URL"):
    
# Database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': os.getenv("PRO_DATABASE_ENGINE"),
        'NAME': os.getenv("PRO_DATABASE_NAME"),
        'USER': os.getenv("PRO_DATABASE_USER"),
        'PASSWORD': os.getenv("PRO_DATABASE_PASSWORD"),
        'HOST': os.getenv("PRO_DATABASE_HOST"),
        'PORT': os.getenv("PRO_DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Static files (CSS, JavaScript, Images)
FORCE_SCRIPT_NAME = '/expense'
STATIC_URL = '/expense/static/'
MEDIA_URL = '/expense/media/'

# Make sure these directories exist
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Whitenoise configuration for production
if os.getenv("DATABASE_URL"):
    # Use the simplest storage class without manifest validation
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    
    # Configure whitenoise
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_ROOT = STATIC_ROOT
    WHITENOISE_INDEX_FILE = True
    # Add static files finders to help locate files
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'expenses.User'

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Expense Management Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Expense Management",
    # Text to put in the sidebar brand section (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Admin",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/favicon.svg",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "images/logo.svg",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "images/favicon.svg",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to Expense Management",
    # Copyright on the footer
    "copyright": "Expense Management ",
    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "expenses.Expense",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "expenses.Expense"},
        # App with dropdown menu to all its models pages
        {"app": "expenses"},
        # External url that opens in new window (Permissions can be added)
        # {"name": "Dashboard", "url": "dashboard", "new_window": False},
        # Separator for the menu
        {"name": "---"},
        # Custom link with dropdown menu
        # {"name": "Reports", "url": "#", "children": [
        #     {"name": "Expense Summary", "url": "admin:expenses_expense_changelist"},
        #     {"name": "Vendor Analysis", "url": "admin:expenses_vendor_changelist"},
        # ]},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/yourusername/expense_management", "new_window": True},
        {"name": "User Guide", "url": "#", "new_window": True},
        {"name": "Profile", "url": "#", "new_window": False},
        {"name": "Logout", "url": "/expense/admin/logout/", "new_window": False, "icon": "fas fa-sign-out-alt"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["expenses", "expenses.User", "expenses.Expense", 
                              "expenses.GLCode","expenses.Head", "expenses.Vendor","expenses.Employee",
                              "expenses.EmployeeType","expenses.Cadre",
                              "expenses.Region", "expenses.Wing","expenses.Division","auth"],
    
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "expenses.Expense": "fas fa-money-bill",
        "expenses.GLCode": "fas fa-file-invoice-dollar",
        "expenses.Vendor": "fas fa-building",
        "expenses.Employee": "fas fa-id-badge",
        "expenses.Region": "fas fa-globe",
        "expenses.Wing": "fas fa-layer-group",
        "expenses.Cadre": "fas fa-calculator",
        "expenses.Division": "fas fa-sitemap",
        "expenses.EmployeeType": "fas fa-id-card",
        "expenses.Head": "fas fa-heading",
        "expenses.User": "fas fa-user-tie",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,
    # Automatically open related modal on page load
    "related_modal_autoheight": True,
    # Show related modal as a form not a grid
    "related_modal_form": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "css/jazzmin-custom.css",
    "custom_js": "js/jazzmin-custom.js",
    # "custom_js": "js/admin-keyboard-navigation.js",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    
    "user_avatar": None,
    # Theme (Use Bootswatch themes or custom CSS)
    "theme": "default",
    # Theme customizations
    "dark_mode_theme": None,
    # UI Customizer options
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "expenses.Expense": "horizontal_tabs",
        "expenses.Vendor": "vertical_tabs",
        "expenses.GLCode": "collapsible",
    },
    # Custom admin dashboard
    "custom_links": {
        "expenses": [{
            "name": "Create New Expense",
            "url": "admin:expenses_expense_add",
            "icon": "fas fa-plus",
            "permissions": ["expenses.add_expense"]
        }, {
            "name": "Vendor Management",
            "url": "admin:expenses_vendor_changelist",
            "icon": "fas fa-building"
        }, {
            "name": "Budget Overview",
            "url": "admin:expenses_glcode_changelist",
            "icon": "fas fa-chart-line"
        }]
    },
    # Custom admin filters
    "list_filter_dropdown": True,
    # Actions on top of list views
    "actions_on_top": True,
    # Actions on bottom of list views
    "actions_on_bottom": False,
    # Save on top of change form
    "save_on_top": True,
}

# Authentication settings
LOGIN_URL = '/expense/login/'
LOGIN_REDIRECT_URL = '/expense/dashboard/'
LOGOUT_REDIRECT_URL = '/expense/login/'  # Add this line to ensure logout redirects to login page

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret"),
    secure=True  
)
