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
                    budgetValues.forEach(el => {
                        el.textContent = '0.00';
                    });
                }
                return response.json();
            })
            .then(data => {
                // Update the budget information in the UI - both amount and amount in millions
                document.getElementById('total-budget').textContent = 
                    formatCurrency(data.total_budget);
                document.getElementById('utilized-budget').textContent = 
                    formatCurrency(data.utilized_budget);
                document.getElementById('available-budget').textContent = 
                    formatCurrency(data.available_budget);
                document.getElementById('monthly-limit').textContent = 
                    formatCurrency(data.monthly_limit);
                
                // Update the million values
                document.getElementById('total-budget-million').textContent = 
                    formatMillions(data.total_budget);
                document.getElementById('utilized-budget-million').textContent = 
                    formatMillions(data.utilized_budget);
                document.getElementById('available-budget-million').textContent = 
                    formatMillions(data.available_budget);
                document.getElementById('monthly-limit-million').textContent = 
                    formatMillions(data.monthly_limit);
            })
            .catch(error => {
                // console.error('Error fetching budget data:', error);
                // Reset to default values on error for both regular and million format values
                budgetValues.forEach(el => {
                    el.textContent = '0.00';
                });
                
                // Also reset the million format values
                document.getElementById('total-budget-million').textContent = '0.000';
                document.getElementById('utilized-budget-million').textContent = '0.000';
                document.getElementById('available-budget-million').textContent = '0.000';
                document.getElementById('monthly-limit-million').textContent = '0.000';
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

    // Helper function to format values in millions
    function formatMillions(value) {
        // Convert to number and handle potential null/undefined
        const num = parseFloat(value || 0) / 1000000;
        
        // Format with commas for thousands and 3 decimal places
        return num.toLocaleString('en-US', {
            minimumFractionDigits: 3,
            maximumFractionDigits: 3
        });
    }
});