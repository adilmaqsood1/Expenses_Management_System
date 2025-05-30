// JavaScript for the add_expense.html form

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    // Initialize the vendor/employee toggle functionality
    initVendorEmployeeToggle();
    
    // Initialize vendor category filtering
    initVendorCategoryFilter();
    
    // Initialize amount calculations
    initAmountCalculations();
    
    // Initialize budget information handling
    initBudgetInfo();
    
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
    const vendorSelectField = document.getElementById('vendor-select-field');
    const employeeField = document.getElementById('employee-field');
    const employeeHeadField = document.getElementById('employee-head-field');
    const employeeWingField = document.getElementById('employee-wing-field');
    const employeeDivisionField = document.getElementById('employee-division-field');
    const employeeCadreField = document.getElementById('employee-cadre-field');
    const employeeTypeField = document.getElementById('employee-type-field');
    
    // Initialize employee data fields when employee is selected
    let employeeSelect = document.getElementById('employee');
    let employeeHeadSelect = document.getElementById('employee_head');
    let employeeWingSelect = document.getElementById('employee_wing');
    let employeeDivisionSelect = document.getElementById('employee_division');
    let employeeCadreSelect = document.getElementById('employee_cadre');
    let employeeTypeSelect = document.getElementById('employee_type');
    
    if (employeeSelect) {
        console.log('Employee select element found');
    } else {
        console.error('Employee select element not found');
    }
    
    // Log which fields were found for debugging
    console.log('Fields found:', {
        vendorField: !!vendorField,
        vendorSelectField: !!vendorSelectField,
        employeeField: !!employeeField,
        employeeHeadField: !!employeeHeadField,
        employeeWingField: !!employeeWingField,
        employeeDivisionField: !!employeeDivisionField,
        employeeCadreField: !!employeeCadreField,
        employeeTypeField: !!employeeTypeField
    });
    
    if (!vendorField || !vendorSelectField || !employeeField) {
        console.error('Required fields not found');
        return;
    }
    
    console.log('Toggle functionality initialized');
    
    // Function to toggle between vendor and employee fields
    function toggleVendorEmployee() {
        console.log('Toggle function called with value:', typeSelect.value);
        
        if (typeSelect.value === 'Employee') {
            // Hide vendor fields
            vendorField.style.display = 'none';
            vendorSelectField.style.display = 'none';
            
            // Show employee fields
            employeeField.style.display = 'block';
            
            // Show employee detail fields (division, wing, sap-id)
            if (employeeHeadField) employeeHeadField.style.display = 'block';
            if (employeeWingField) employeeWingField.style.display = 'block';
            if (employeeDivisionField) employeeDivisionField.style.display = 'block';
            if (employeeCadreField) employeeCadreField.style.display = 'block';
            if (employeeTypeField) employeeTypeField.style.display = 'block';
            
            // Show employee details section
            const employeeDetailsSection = document.getElementById('employee-details-section');
            if (employeeDetailsSection) {
                employeeDetailsSection.style.display = 'block';
            }
            
            // Initialize employee filtering
            initEmployeeFiltering();
            
            // Update the form header
            updateFormHeader('Employee');
        } else {
            // Hide employee fields
            employeeField.style.display = 'none';
            
            // Hide employee detail fields (division, wing, sap-id)
            if (employeeHeadField) employeeHeadField.style.display = 'none';
            if (employeeWingField) employeeWingField.style.display = 'none';
            if (employeeDivisionField) employeeDivisionField.style.display = 'none';
            
            // Hide employee details section
            const employeeDetailsSection = document.getElementById('employee-details-section');
            if (employeeDetailsSection) {
                employeeDetailsSection.style.display = 'none';
            }
            
            // Show vendor fields
            vendorField.style.display = '';
            vendorSelectField.style.display = '';
            
            // Update the form header
            updateFormHeader('Vendor');
        }
        
        // Log the current display states for debugging
        console.log('Current display states:', {
            vendorField: vendorField.style.display,
            vendorSelectField: vendorSelectField.style.display,
            employeeField: employeeField.style.display,
            employeeHeadField: employeeHeadField ? employeeHeadField.style.display : 'not found',
            employeeWingField: employeeWingField ? employeeWingField.style.display : 'not found',
            employeeDivisionField: employeeDivisionField ? employeeDivisionField.style.display : 'not found'
        });
    }
    
    // Function to initialize employee filtering based on head, wing, and division
    function initEmployeeFiltering() {
        if (!employeeHeadSelect || !employeeWingSelect || !employeeDivisionSelect || !employeeSelect) {
            console.error('One or more employee filter elements not found');
            return;
        }
        
        // Store all employee options for filtering
        const allEmployeeOptions = Array.from(employeeSelect.options);
        
        // Function to filter employees based on selected criteria
        function filterEmployees() {
            const selectedHead = employeeHeadSelect.value;
            const selectedWing = employeeWingSelect.value;
            const selectedDivision = employeeDivisionSelect.value;
            
            console.log('Filtering employees with criteria:', {
                head: selectedHead,
                wing: selectedWing,
                division: selectedDivision
            });
            
            // Clear current options
            employeeSelect.innerHTML = '';
            
            // Filter and add matching employees
            allEmployeeOptions.forEach(option => {
                const employeeHead = option.getAttribute('data-head');
                const employeeWing = option.getAttribute('data-wing');
                const employeeDivision = option.getAttribute('data-division');
                
                // Check if the employee matches the selected criteria
                // If a criterion is empty, don't filter by it
                const headMatches = !selectedHead || employeeHead === selectedHead;
                const wingMatches = !selectedWing || employeeWing === selectedWing;
                const divisionMatches = !selectedDivision || employeeDivision === selectedDivision;
                
                if (headMatches && wingMatches && divisionMatches) {
                    employeeSelect.appendChild(option.cloneNode(true));
                }
            });
            
            // If no options were added, show a message
            if (employeeSelect.options.length === 0) {
                const noOption = document.createElement('option');
                noOption.text = 'No employees match the selected criteria';
                noOption.value = '';
                employeeSelect.appendChild(noOption);
            }
        }
        
        // Add event listeners for head, wing, and division changes
        employeeHeadSelect.addEventListener('change', filterEmployees);
        employeeWingSelect.addEventListener('change', filterEmployees);
        employeeDivisionSelect.addEventListener('change', filterEmployees);
        
        // Run the filter function initially
        filterEmployees();
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
    
    // Add functionality to populate employee fields when an employee is selected
    // Use the employeeSelect variable that was already defined
    if (employeeSelect) {
        // Remove any existing event listeners before adding a new one
        employeeSelect.removeEventListener('change', updateEmployeeFields);
        
        // Define the function to update employee fields
        function updateEmployeeFields() {
            const selectedOption = this.options[this.selectedIndex];
            
            // Only update fields if a valid employee is selected
            if (selectedOption && selectedOption.value) {
                console.log('Employee change event triggered', {
                    head: selectedOption.getAttribute('data-head'),
                    wing: selectedOption.getAttribute('data-wing'),
                    division: selectedOption.getAttribute('data-division')
                });
            }
        }
        
        // Add the event listener directly to the original element
        employeeSelect.addEventListener('change', updateEmployeeFields);
    }
    
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
        netAmountInput.value = netAmount.toFixed();
        console.log('Net amount calculated:', netAmount);
    }
    
    // Add event listeners for input changes
    amountInput.addEventListener('input', calculateNetAmount);
    amountInput.addEventListener('change', calculateNetAmount);
    
    // Only add listeners if the elements exist
    if (salesTaxInput) salesTaxInput.addEventListener('input', calculateNetAmount);
    if (incomeTaxInput) incomeTaxInput.addEventListener('input', calculateNetAmount);
    
    // If tax inputs don't exist, set up direct copy from amount to net amount
    if (!salesTaxInput && !incomeTaxInput) {
        console.log('Tax inputs not found, setting up direct amount copy');
        amountInput.addEventListener('input', function() {
            const amount = parseFloat(this.value) || 0;
            netAmountInput.value = amount.toFixed();
        });
    }
    
    // Calculate net amount on page load to ensure it's populated
    calculateNetAmount();
}

/**
 * Initialize budget information handling
 */
function initBudgetInfo() {
    // Get the head select element
    const headSelect = document.getElementById('head');
    
    // If we're on the add expense page and the head select exists
    if (headSelect) {
        // Add event listener for head selection change
        headSelect.addEventListener('change', updateBudgetInfo);
        
        // Initial update of budget info based on the default selected head
        updateBudgetInfo();
    }
    
    // Add event listener for amount field to update budget status when amount changes
    const amountField = document.getElementById('amount');
    if (amountField) {
        amountField.addEventListener('input', updateBudgetStatus);
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
        document.getElementById('budget-status').textContent = 'Pending';
        
        // Update the budget table title to show which head's budget is being displayed
        const selectedOption = headSelect.options[headSelect.selectedIndex];
        const headName = selectedOption.text;
        document.querySelector('.total-budget-row td:first-child').textContent = `Total Budget (${headName})`;
        document.querySelector('.utilized-budget-row td:first-child').textContent = `Utilized Budget (${headName})`;
        document.querySelector('.available-budget-row td:first-child').textContent = `Available Budget (${headName})`;
        
        // Fetch budget information from the server
        fetch(`/expense/expense/api/head-budget/${headId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update the budget information in the UI
                document.getElementById('total-budget').textContent = formatCurrency(data.total_budget);
                document.getElementById('utilized-budget').textContent = formatCurrency(data.utilized_budget);
                document.getElementById('available-budget').textContent = formatCurrency(data.available_budget);
                document.getElementById('monthly-limit').textContent = formatCurrency(data.monthly_limit);
                
                // Update the hidden form fields
                document.getElementById('hidden-total-budget').value = data.total_budget || 0;
                document.getElementById('hidden-utilized-budget').value = data.utilized_budget || 0;
                document.getElementById('hidden-available-budget').value = data.available_budget || 0;
                document.getElementById('hidden-monthly-limit').value = data.monthly_limit || 0;
                
                // Determine budget status
                let budgetStatus = 'Pending';
                if (data.available_budget > 0) {
                    const amountField = document.getElementById('amount');
                    const amount = parseFloat(amountField?.value || 0);
                    
                    if (amount <= data.available_budget) {
                        budgetStatus = 'Approved';
                    } else {
                        budgetStatus = 'Rejected';
                    }
                } else {
                    budgetStatus = 'Rejected';
                }
                
                // Update budget status display and hidden field
                document.getElementById('budget-status').textContent = budgetStatus;
                document.getElementById('hidden-budget-status').value = budgetStatus;
                
                // Apply styling based on budget status
                const budgetStatusElement = document.getElementById('budget-status');
                budgetStatusElement.className = ''; // Clear existing classes
                
                if (budgetStatus === 'Approved') {
                    budgetStatusElement.classList.add('status-approved');
                } else if (budgetStatus === 'Rejected') {
                    budgetStatusElement.classList.add('status-rejected');
                } else {
                    budgetStatusElement.classList.add('status-pending');
                }
            })
            .catch(error => {
                console.error('Error fetching budget data:', error);
                
                // Reset to default values on error
                document.getElementById('total-budget').textContent = '0';
                document.getElementById('utilized-budget').textContent = '0';
                document.getElementById('available-budget').textContent = '0';
                document.getElementById('monthly-limit').textContent = '0';
                document.getElementById('budget-status').textContent = 'Pending';
                
                // Reset hidden fields
                document.getElementById('hidden-total-budget').value = 0;
                document.getElementById('hidden-utilized-budget').value = 0;
                document.getElementById('hidden-available-budget').value = 0;
                document.getElementById('hidden-monthly-limit').value = 0;
                document.getElementById('hidden-budget-status').value = 'Pending';
            });
    }
    
    // Function to update budget status based on amount
    function updateBudgetStatus() {
        const availableBudget = parseFloat(document.getElementById('hidden-available-budget').value || 0);
        const amount = parseFloat(amountField.value || 0);
        
        let budgetStatus = 'Pending';
        if (availableBudget > 0) {
            if (amount <= availableBudget) {
                budgetStatus = 'Approved';
            } else {
                budgetStatus = 'Rejected';
            }
        } else {
            budgetStatus = 'Rejected';
        }
        
        // Update budget status display and hidden field
        document.getElementById('budget-status').textContent = budgetStatus;
        document.getElementById('hidden-budget-status').value = budgetStatus;
        
        // Apply styling based on budget status
        const budgetStatusElement = document.getElementById('budget-status');
        budgetStatusElement.className = ''; // Clear existing classes
        
        if (budgetStatus === 'Approved') {
            budgetStatusElement.classList.add('status-approved');
        } else if (budgetStatus === 'Rejected') {
            budgetStatusElement.classList.add('status-rejected');
        } else {
            budgetStatusElement.classList.add('status-pending');
        }
    }
    
    // Helper function to format currency values
    function formatCurrency(value) {
        // Convert to number and handle potential null/undefined
        const num = parseFloat(value || 0);
        
        // Check if the number has decimal part
        if (num % 1 === 0) {
            // If it's a whole number, don't show decimal places
            return num.toLocaleString('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });
        } else {
            // If it has decimal part, show up to 2 decimal places
            return num.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }
    }
}

// Update the form submission event listener to show more detailed error
expenseForm.addEventListener('submit', function(event) {
    // Get available budget and amount values
    const availableBudgetElement = document.getElementById('available-budget');
    const amountInput = document.getElementById('amount');
    
    if (availableBudgetElement && amountInput) {
        const availableBudgetText = availableBudgetElement.textContent;
        const availableBudget = parseFloat(availableBudgetText.replace(/[^0-9.-]+/g, ''));
        const expenseAmount = parseFloat(amountInput.value);
        
        // Check if expense amount exceeds available budget
        if (!isNaN(availableBudget) && !isNaN(expenseAmount) && expenseAmount > availableBudget) {
            // Show error message with detailed information
            const errorMessage = document.getElementById('budget-error-message');
            const errorDetails = document.getElementById('budget-error-details');
            
            if (errorMessage && errorDetails) {
                // Format the amounts with commas for better readability
                const formattedBudget = availableBudget.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                const formattedAmount = expenseAmount.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                
                // Set detailed error message
                errorDetails.innerHTML = `Your expense amount <strong>${formattedAmount}</strong> exceeds the available budget <strong>${formattedBudget}</strong>. Please contact your admin to increase the budget allocation.`;
                
                // Show the error message
                errorMessage.style.display = 'block';
            }
            
            // Prevent form submission
            event.preventDefault();
            
            // Scroll to error message
            errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
});