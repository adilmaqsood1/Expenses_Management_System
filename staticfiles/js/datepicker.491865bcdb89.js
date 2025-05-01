// Date picker implementation for expense management system

document.addEventListener('DOMContentLoaded', function() {
    // Add jQuery UI datepicker if it's not already included
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

    // Check if jQuery is already loaded
    if (typeof jQuery === 'undefined') {
        loadScript('https://code.jquery.com/jquery-3.6.0.min.js', function() {
            loadJqueryUI();
        });
    } else {
        loadJqueryUI();
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
        // Initialize datepickers for expense list page
        const startDateInput = document.querySelector('.search-form .form-group:nth-child(1) input');
        const endDateInput = document.querySelector('.search-form .form-group:nth-child(2) input');

        if (startDateInput && endDateInput) {
            // Add calendar icon to the date inputs
            addCalendarIcon(startDateInput);
            addCalendarIcon(endDateInput);

            // Initialize jQuery UI datepicker
            $(startDateInput).datepicker({
                dateFormat: 'd M yy',
                changeMonth: true,
                changeYear: true,
                onSelect: function(dateText) {
                    // Update the min date of the end date picker
                    $(endDateInput).datepicker('option', 'minDate', dateText);
                }
            });

            $(endDateInput).datepicker({
                dateFormat: 'd M yy',
                changeMonth: true,
                changeYear: true,
                onSelect: function(dateText) {
                    // Update the max date of the start date picker
                    $(startDateInput).datepicker('option', 'maxDate', dateText);
                }
            });

            // Set initial values
            const currentDate = new Date();
            $(startDateInput).datepicker('setDate', currentDate);
            $(endDateInput).datepicker('setDate', currentDate);
        }

        // Also initialize datepicker for invoice_date in add_expense page if it exists
        const invoiceDateInput = document.getElementById('invoice_date');
        if (invoiceDateInput) {
            addCalendarIcon(invoiceDateInput);
            $(invoiceDateInput).datepicker({
                dateFormat: 'd/m/yy',
                changeMonth: true,
                changeYear: true
            });
        }
    }

    function addCalendarIcon(inputElement) {
        // Create a wrapper div for the input
        const wrapper = document.createElement('div');
        wrapper.className = 'date-input-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';
        wrapper.style.width = '100%';
        
        // Clone the input element to preserve its attributes and value
        const newInput = inputElement.cloneNode(true);
        newInput.style.paddingRight = '30px'; // Make room for the icon
        
        // Create the calendar icon
        const icon = document.createElement('span');
        icon.innerHTML = '📅';
        icon.style.position = 'absolute';
        icon.style.right = '5px';
        icon.style.top = '50%';
        icon.style.transform = 'translateY(-50%)';
        icon.style.cursor = 'pointer';
        icon.style.zIndex = '1';
        
        // Replace the input with our wrapper
        inputElement.parentNode.replaceChild(wrapper, inputElement);
        
        // Add the new input and icon to the wrapper
        wrapper.appendChild(newInput);
        wrapper.appendChild(icon);
        
        // Make the icon click open the datepicker
        icon.addEventListener('click', function() {
            $(newInput).datepicker('show');
        });
        
        return newInput;
    }
});