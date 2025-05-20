from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        extra_fields.setdefault('role', 'USER')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    # Role choices
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MAKERS', 'Makers'),
        ('SUPERVISOR', 'Supervisor'),
        ('MIS', 'MIS'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    account_number = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=100, blank=True, null=True)
    wing = models.ForeignKey('expenses.Wing', on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey('expenses.Division', on_delete=models.SET_NULL, null=True, blank=True)
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # Check if this is a new user (no ID) or the password has been changed
        if not self.pk or self._password is not None:
            # Only hash the password if it's not already hashed
            if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
                self.set_password(self.password)
        super().save(*args, **kwargs)
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_maker(self):
        return self.role == 'MAKERS'
    
    @property
    def is_supervisor(self):
        return self.role == 'SUPERVISOR'
    
    @property
    def is_mis(self):
        return self.role == 'MIS'
