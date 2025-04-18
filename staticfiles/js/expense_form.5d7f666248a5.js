// JavaScript for the add_expense.html form

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    // Initialize the vendor/employee toggle functionality
    initVendorEmployeeToggle();
    
    // Initialize vendor category filtering
    initVendorCategoryFilter();
    
    // Initialize amount calculations
    initAmountCalculations();
    
    // Run toggle again after a short delay to ensure it works
    setTimeout(function() {
        console.log('Running delayed initialization');
        initVendorEmployeeToggle();
        initVendorCategoryFilter();
    }, 1000);
});

// Add a fallback initialization for browsers that might have issues
window.onload = function() {
    console.log('Window fully loaded - fallback initialization');
    initVendorEmployeeToggle();
    initVendorCategoryFilter();
};

/**
 * Initialize the vendor category filter functionality
 */
function initVendorCategoryFilter() {
    const categorySelect = document.getElementById('vendor_category');
    const vendorSelect = document.getElementById('vendor');
    
    if (!categorySelect || !vendorSelect) {
        console.error('Category or vendor select elements not found');
        return;
    }
    
    console.log('Vendor category filter initialized');
    
    // Store all vendor options for later filtering
    const allVendorOptions = Array.from(vendorSelect.options);
    
    // Function to filter vendors based on selected category
    function filterVendorsByCategory() {
        const selectedCategory = categorySelect.value;
        console.log('Filtering vendors by category:', selectedCategory);
        
        // Clear current options
        vendorSelect.innerHTML = '';
        
        // Filter and add matching vendors
        allVendorOptions.forEach(option => {
            const vendorCategory = option.getAttribute('data-category');
            
            // If category matches or is 'General' (when no specific category is selected)
            if (selectedCategory === 'General' || vendorCategory === selectedCategory) {
                vendorSelect.appendChild(option.cloneNode(true));
            }
        });
        
        // If no options were added, show a message
        if (vendorSelect.options.length === 0) {
            const noOption = document.createElement('option');
            noOption.text = 'No vendors available for this category';
            noOption.value = '';
            vendorSelect.appendChild(noOption);
        }
    }
    
    // Run the filter function on page load
    filterVendorsByCategory();
    
    // Add event listener for category changes
    categorySelect.addEventListener('change', filterVendorsByCategory);
}

/**
 * Initialize the vendor/employee toggle functionality
 */
function initVendorEmployeeToggle() {
    // Get the type select element
    const typeSelect = document.getElementById('type');
    if (!typeSelect) {
        console.error('Type select element not found');
        return;
    }
    
    // Get the vendor and employee field elements
    const vendorField = document.getElementById('vendor-field');
    const employeeField = document.getElementById('employee-field');
    
    if (!vendorField || !employeeField) {
        console.error('Vendor or employee field not found', {
            vendorField: !!vendorField,
            employeeField: !!employeeField
        });
        return;
    }
    
    console.log('Toggle functionality initialized');
    
    // Function to toggle between vendor and employee fields
    function toggleVendorEmployee() {
        console.log('Toggle function called with value:', typeSelect.value);
        
        // Get both vendor-related fields directly using the correct IDs from the HTML
        const vendorCategoryField = document.getElementById('vendor-field');
        const vendorSelectField = document.getElementById('vendor-select-field');
        
        // Make sure we have all required elements
        if (!vendorCategoryField || !vendorSelectField) {
            console.error('Vendor category or select field not found');
            return;
        }
        
        // Force display style to be a string value
        if (typeSelect.value === 'Employee') {
            // Hide both vendor fields - use !important to override any inline styles
            vendorCategoryField.style.cssText = 'display: none !important';
            vendorSelectField.style.cssText = 'display: none !important';
            employeeField.style.cssText = 'display: block !important';
            // Update the form header to show the selected type
            updateFormHeader('Employee');
        } else {
            // Show both vendor fields
            vendorCategoryField.style.cssText = 'display: block !important';
            vendorSelectField.style.cssText = 'display: block !important';
            employeeField.style.cssText = 'display: none !important';
            // Update the form header to show the selected type
            updateFormHeader('Vendor');
        }
        
        // Log the current display states for debugging
        console.log('Current display states:', {
            vendorCategory: vendorCategoryField.style.display,
            vendorSelect: vendorSelectField.style.display,
            employee: employeeField.style.display,
            typeValue: typeSelect.value
        });
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
    
    // Add a direct click handler as a backup
    typeSelect.onclick = function() {
        setTimeout(toggleVendorEmployee, 100); // Small delay to ensure value is updated
    };
    
    // Run again after a short delay to ensure proper initialization
    setTimeout(toggleVendorEmployee, 500);
}

/**
 * Initialize amount calculations
 */
function initAmountCalculations() {
    const amountInput = document.getElementById('amount');
    const netAmountInput = document.getElementById('net_amount');
    
    // Check if the withholding tax inputs exist (they might be commented out in the HTML)
    const salesTaxInput = document.getElementById('withholding_sales_tax');
    const incomeTaxInput = document.getElementById('withholding_income_tax');
    
    if (!amountInput || !netAmountInput) {
        console.error('Required amount inputs not found', {
            amountInput: !!amountInput,
            netAmountInput: !!netAmountInput
        });
        return;
    }
    
    console.log('Amount calculation initialized');
    
    // Function to calculate net amount
    function calculateNetAmount() {
        const amount = parseFloat(amountInput.value) || 0;
        let salesTax = 0;
        let incomeTax = 0;
        
        // Only use tax values if the elements exist
        if (salesTaxInput) salesTax = parseFloat(salesTaxInput.value) || 0;
        if (incomeTaxInput) incomeTax = parseFloat(incomeTaxInput.value) || 0;
        
        const netAmount = amount - salesTax - incomeTax;
        netAmountInput.value = netAmount.toFixed(2);
        console.log('Net amount calculated:', netAmount);
    }
    
    // Add event listeners for input changes
    amountInput.addEventListener('input', calculateNetAmount);
    
    // Only add listeners if the elements exist
    if (salesTaxInput) salesTaxInput.addEventListener('input', calculateNetAmount);
    if (incomeTaxInput) incomeTaxInput.addEventListener('input', calculateNetAmount);
    
    // If tax inputs don't exist, set up direct copy from amount to net amount
    if (!salesTaxInput && !incomeTaxInput) {
        console.log('Tax inputs not found, setting up direct amount copy');
        amountInput.addEventListener('input', function() {
            netAmountInput.value = amountInput.value;
        });
    }
}