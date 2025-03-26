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
        const budgetValues = document.querySelectorAll('.budget-value');
        budgetValues.forEach(el => {
            el.textContent = 'Loading...';
        });
        
        // Fetch budget information from the server
        fetch(`/api/head-budget/${headId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update the budget information in the UI
                document.getElementById('total-budget').textContent = 
                    formatCurrency(data.total_budget);
                document.getElementById('utilized-budget').textContent = 
                    formatCurrency(data.utilized_budget);
                document.getElementById('available-budget').textContent = 
                    formatCurrency(data.available_budget);
                document.getElementById('monthly-limit').textContent = 
                    formatCurrency(data.monthly_limit);
            })
            .catch(error => {
                console.error('Error fetching budget data:', error);
                // Reset to default values on error
                budgetValues.forEach(el => {
                    el.textContent = '0.00';
                });
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