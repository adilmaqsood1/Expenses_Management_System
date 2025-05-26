// JavaScript for handling dynamic budget information in the expense form

document.addEventListener('DOMContentLoaded', function() {
    // Get the head select element
    const headSelect = document.getElementById('head');
    
    // If we're on the add expense page and the head select exists
    if (headSelect) {
        // Add event listener for head selection change
        headSelect.addEventListener('change', updateBudgetInfo);
        
        // Initial update of budget info based on the default selected head
        updateBudgetInfo();
    }
    
    // Function to update budget information based on selected head
    function updateBudgetInfo() {
        const headId = headSelect.value;
        if (!headId) return;
        
        // Show loading state
        document.getElementById('total-budget').textContent = 'Loading...';
        document.getElementById('utilized-budget').textContent = 'Loading...';
        document.getElementById('available-budget').textContent = 'Loading...';
        document.getElementById('monthly-limit').textContent = 'Loading...';
        document.getElementById('budget-status').textContent = 'Loading...';
        
        // Fetch budget information from the server
        fetch(`/api/head-budget/${headId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {

                console.log('Received data:', data);
                // Update the budget information in the UI
                document.getElementById('total-budget').textContent = formatCurrency(data.total_budget);
                document.getElementById('utilized-budget').textContent = formatCurrency(data.utilized_budget);
                document.getElementById('available-budget').textContent = formatCurrency(data.available_budget);
                document.getElementById('monthly-limit').textContent = formatCurrency(data.monthly_limit);
                
                // Update budget status with color coding
                const budgetStatus = document.getElementById('budget-status');
                budgetStatus.textContent = data.budget_status;
                
                if (data.budget_status === 'Available') {
                    budgetStatus.style.color = 'green';
                } else {
                    budgetStatus.style.color = 'red';
                }
                
                // Update hidden fields for form submission
                document.getElementById('hidden-total-budget').value = data.total_budget;
                document.getElementById('hidden-utilized-budget').value = data.utilized_budget;
                document.getElementById('hidden-available-budget').value = data.available_budget;
                document.getElementById('hidden-monthly-limit').value = data.monthly_limit;
                document.getElementById('hidden-budget-status').value = data.budget_status;
            })
            .catch(error => {
                console.error('Error fetching budget data:', error);
                
                // Reset to default values on error
                document.getElementById('total-budget').textContent = '0';
                document.getElementById('utilized-budget').textContent = '0';
                document.getElementById('available-budget').textContent = '0';
                document.getElementById('monthly-limit').textContent = '0';
                document.getElementById('budget-status').textContent = 'Unknown';
                
                // Reset hidden fields
                document.getElementById('hidden-total-budget').value = '0';
                document.getElementById('hidden-utilized-budget').value = '0';
                document.getElementById('hidden-available-budget').value = '0';
                document.getElementById('hidden-monthly-limit').value = '0';
                document.getElementById('hidden-budget-status').value = 'Unknown';
            });
    }
    
    // Helper function to format currency values
    function formatCurrency(value) {
        // Convert to number and handle potential null/undefined
        const num = parseFloat(value || 0);
        
        // Format with commas for thousands and 2 decimal places
        return num.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
});