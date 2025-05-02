from django.db import migrations, models
from decimal import Decimal

def calculate_initial_values(apps, schema_editor):
    Head = apps.get_model('expenses', 'Head')
    Expense = apps.get_model('expenses', 'Expense')
    
    for head in Head.objects.all():
        # Calculate utilized budget from approved expenses
        utilized = Expense.objects.filter(
            head=head,
            status='Approved'
        ).aggregate(models.Sum('amount'))['amount__sum'] or Decimal('0')
        
        # Set the values
        head.utilized_budget = utilized
        head.remaining_budget = head.budget - utilized
        head.save()

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0017_remove_expense_sub_head_expense_admin_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='head',
            name='utilized_budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='head',
            name='remaining_budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.RunPython(calculate_initial_values),
    ]