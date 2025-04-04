// JavaScript for the add_expense.html form

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the vendor/employee toggle functionality
    initVendorEmployeeToggle();
    
    // Initialize amount calculations
    initAmountCalculations();
});

/**
 * Initialize the vendor/employee toggle functionality
 */
function initVendorEmployeeToggle() {
    const typeSelect = document.getElementById('type');
    if (!typeSelect) return;
    
    const vendorField = document.getElementById('vendor-field');
    const employeeField = document.getElementById('employee-field');
    
    if (!vendorField || !employeeField) return;
    
    // Function to toggle between vendor and employee fields
    function toggleVendorEmployee() {
        if (typeSelect.value === 'Employee') {
            vendorField.style.display = 'none';
            employeeField.style.display = 'block';
            // Update the form header to show the selected type
            updateFormHeader('Employee');
        } else {
            vendorField.style.display = 'block';
            employeeField.style.display = 'none';
            // Update the form header to show the selected type
            updateFormHeader('Vendor');
        }
    }
    
    // Function to update the form header
    function updateFormHeader(type) {
        const expenseHeader = document.querySelector('.expense-header');
        if (expenseHeader) {
            expenseHeader.textContent = `Expense Posting - ${type}`;
        }
    }
    
    // Run the function on page load to set initial state
    toggleVendorEmployee();
    
    // Add event listener for changes
    typeSelect.addEventListener('change', toggleVendorEmployee);
}

/**
 * Initialize amount calculations
 */
function initAmountCalculations() {
    const amountInput = document.getElementById('amount');
    const salesTaxInput = document.getElementById('withholding_sales_tax');
    const incomeTaxInput = document.getElementById('withholding_income_tax');
    const netAmountInput = document.getElementById('net_amount');
    
    if (!amountInput || !salesTaxInput || !incomeTaxInput || !netAmountInput) return;
    
    // Function to calculate net amount
    function calculateNetAmount() {
        const amount = parseFloat(amountInput.value) || 0;
        const salesTax = parseFloat(salesTaxInput.value) || 0;
        const incomeTax = parseFloat(incomeTaxInput.value) || 0;
        
        const netAmount = amount - salesTax - incomeTax;
        netAmountInput.value = netAmount.toFixed(2);
    }
    
    // Add event listeners for input changes
    amountInput.addEventListener('input', calculateNetAmount);
    salesTaxInput.addEventListener('input', calculateNetAmount);
    incomeTaxInput.addEventListener('input', calculateNetAmount);
}