// Enhanced JavaScript for expense list page

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the vendor/employee toggle functionality
    initVendorEmployeeToggle();
    
    // Initialize enhanced datepickers
    initEnhancedDatepickers();
    
    // Initialize table features
    initTableFeatures();
    
    // Initialize mobile responsiveness
    initMobileResponsiveness();
    
    // Initialize real-time search
    initRealTimeSearch();
});

/**
 * Initialize the vendor/employee toggle functionality
 */
function initVendorEmployeeToggle() {
    const typeSelect = document.getElementById('expenseType');
    if (!typeSelect) return;
    
    function toggleVendorEmployee() {
        const vendorGroup = document.getElementById('vendorGroup');
        const employeeGroup = document.getElementById('employeeGroup');
        const vendorSelect = document.getElementById('vendorSelect');
        const employeeSelect = document.getElementById('employeeSelect');
        
        if (typeSelect.value.toLowerCase() === 'employee') {
            vendorGroup.style.display = 'none';
            employeeGroup.style.display = 'block';
            vendorSelect.name = '';
            employeeSelect.name = 'employee';
            
            // Add animation
            employeeGroup.classList.add('animate-fade-in');
        } else {
            vendorGroup.style.display = 'block';
            employeeGroup.style.display = 'none';
            vendorSelect.name = 'vendor';
            employeeSelect.name = '';
            
            // Add animation
            vendorGroup.classList.add('animate-fade-in');
        }
    }
    
    // Run the function on page load to set initial state
    toggleVendorEmployee();
    
    // Add event listener for changes
    typeSelect.addEventListener('change', toggleVendorEmployee);
}

/**
 * Initialize enhanced datepickers
 */
function initEnhancedDatepickers() {
    // Check if jQuery and jQuery UI are available
    if (typeof jQuery === 'undefined') {
        loadScript('https://code.jquery.com/jquery-3.6.0.min.js', function() {
            loadJqueryUI();
        });
    } else {
        loadJqueryUI();
    }
    
    function loadScript(url, callback) {
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = url;
        script.onload = callback;
        document.head.appendChild(script);
    }
    
    function loadStylesheet(url) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = url;
        document.head.appendChild(link);
    }
    
    function loadJqueryUI() {
        if (typeof jQuery.ui === 'undefined') {
            loadStylesheet('https://code.jquery.com/ui/1.13.2/themes/base/jquery-ui.css');
            loadScript('https://code.jquery.com/ui/1.13.2/jquery-ui.min.js', initDatepickers);
        } else {
            initDatepickers();
        }
    }
    
    function initDatepickers() {
        // Find date inputs
        const startDateInput = document.querySelector('.search-form input[name="start_date"]');
        const endDateInput = document.querySelector('.search-form input[name="end_date"]');
        
        if (startDateInput && endDateInput) {
            // Add calendar icon and styling
            enhanceDateInput(startDateInput);
            enhanceDateInput(endDateInput);
            
            // Initialize jQuery UI datepicker with enhanced options
            $(startDateInput).datepicker({
                dateFormat: 'yy-mm-dd',
                changeMonth: true,
                changeYear: true,
                showOtherMonths: true,
                selectOtherMonths: true,
                onSelect: function(dateText) {
                    // Update the min date of the end date picker
                    $(endDateInput).datepicker('option', 'minDate', dateText);
                    
                    // Trigger change event for real-time filtering
                    startDateInput.dispatchEvent(new Event('change'));
                }
            });
            
            $(endDateInput).datepicker({
                dateFormat: 'yy-mm-dd',
                changeMonth: true,
                changeYear: true,
                showOtherMonths: true,
                selectOtherMonths: true,
                onSelect: function(dateText) {
                    // Update the max date of the start date picker
                    $(startDateInput).datepicker('option', 'maxDate', dateText);
                    
                    // Trigger change event for real-time filtering
                    endDateInput.dispatchEvent(new Event('change'));
                }
            });
        }
    }
    
    function enhanceDateInput(inputElement) {
        // Create a wrapper div
        const wrapper = document.createElement('div');
        wrapper.className = 'date-input-wrapper relative';
        
        // Clone the input
        const newInput = inputElement.cloneNode(true);
        newInput.classList.add('pr-10'); // Add padding for the icon
        
        // Create the calendar icon
        const icon = document.createElement('div');
        icon.className = 'date-icon absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none';
        icon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
        `;
        
        // Replace the original input with the wrapper
        inputElement.parentNode.replaceChild(wrapper, inputElement);
        
        // Add the new input and icon to the wrapper
        wrapper.appendChild(newInput);
        wrapper.appendChild(icon);
    }
}

/**
 * Initialize table features
 */
function initTableFeatures() {
    const table = document.getElementById('expenseTable');
    if (!table) return;
    
    // Make table headers sticky
    const thead = table.querySelector('thead');
    if (thead) {
        thead.classList.add('sticky', 'top-0', 'z-10');
    }
    
    // Add hover effect to table rows
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.classList.add('hover:bg-cyan-50', 'transition-colors', 'duration-150');
    });
    
    // Enhance the empty state message
    const emptyRow = table.querySelector('tbody tr td[colspan="12"]');
    if (emptyRow) {
        emptyRow.innerHTML = `
            <div class="flex flex-col items-center justify-center py-12">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p class="text-gray-500 text-lg font-medium">No expenses found</p>
                <p class="text-gray-400 text-sm mt-1">Try adjusting your search filters</p>
                <a href="{% url 'add_expense' %}" class="mt-4 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
                    </svg>
                    Add New Expense
                </a>
            </div>
        `;
    }
}

/**
 * Initialize mobile responsiveness
 */
function initMobileResponsiveness() {
    // Create filter toggle button for mobile
    const searchForm = document.querySelector('.search-form');
    if (!searchForm) return;
    
    const filterToggle = document.createElement('button');
    filterToggle.className = 'filter-toggle';
    filterToggle.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd" />
        </svg>
        <span>Toggle Filters</span>
    `;
    
    // Insert before the search form
    searchForm.parentNode.insertBefore(filterToggle, searchForm);
    
    // Add event listener to toggle the search form
    filterToggle.addEventListener('click', function() {
        searchForm.classList.toggle('show');
        
        // Change button text based on form visibility
        const buttonText = searchForm.classList.contains('show') ? 'Hide Filters' : 'Show Filters';
        filterToggle.querySelector('span').textContent = buttonText;
    });
    
    // Make table responsive
    const tableContainer = document.querySelector('.overflow-x-auto');
    if (tableContainer) {
        tableContainer.classList.add('responsive-table');
    }
}

/**
 * Initialize real-time search functionality
 */
function initRealTimeSearch() {
    const form = document.getElementById('expenseFilterForm');
    if (!form) return;
    
    // Add debounce function to prevent excessive API calls
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    // Function to handle form input changes
    const handleFormChange = debounce(function() {
        // In a real implementation, this would make an AJAX call to filter results
        // For now, we'll just submit the form
        form.submit();
    }, 500);
    
    // Add event listeners to form inputs
    const formInputs = form.querySelectorAll('input, select');
    formInputs.forEach(input => {
        if (input.type !== 'submit') {
            input.addEventListener('change', handleFormChange);
        }
    });
}

// Add CSS classes for animations
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .animate-fade-in {
            animation: fadeIn 0.3s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});