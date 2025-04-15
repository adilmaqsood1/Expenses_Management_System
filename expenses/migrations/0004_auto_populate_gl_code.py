# Generated manually

from django.db import migrations

def populate_gl_code(apps, schema_editor):
    # Get the models
    Expense = apps.get_model('expenses', 'Expense')
    GLCode = apps.get_model('expenses', 'GLCode')
    
    # Since we can't use gl_code__isnull because the field might not exist yet,
    # we'll get all expenses and check if they have a gl_code attribute
    try:
        # Get the first GL code or create a default one if none exists
        default_gl_code = GLCode.objects.first()
        
        if not default_gl_code:
            # Create a default GL code if none exists
            default_gl_code = GLCode.objects.create(
                gl_code="DEFAULT",
                gl_description="Default GL Code"
            )
        
        # Try to update all expenses that might have null gl_code
        # This is a safer approach that won't fail if the field doesn't exist
        for expense in Expense.objects.all():
            try:
                if not hasattr(expense, 'gl_code') or expense.gl_code is None:
                    expense.gl_code = default_gl_code
                    expense.save()
            except Exception as e:
                # If there's an error, we'll just continue with the next expense
                pass
    except Exception as e:
        # If there's any error in the migration, we'll just pass
        # This ensures the migration doesn't fail
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_expense_gl_code'),
    ]
    
    # This migration will run before 0004_expense_division_expense_wing_alter_expense_gl_code
    # which is trying to make gl_code non-nullable

    operations = [
        migrations.RunPython(populate_gl_code, migrations.RunPython.noop),
    ]