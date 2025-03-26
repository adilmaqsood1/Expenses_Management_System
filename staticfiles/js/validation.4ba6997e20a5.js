// Validation script for expense management system

document.addEventListener('DOMContentLoaded', function() {
    // Integer-only validation for CNIC and GL Code fields
    
    // Find CNIC input fields
    const cnicInputs = document.querySelectorAll('input[name="cnic"]');
    
    // Find GL Code input fields that are not readonly
    const glCodeInputs = document.querySelectorAll('input[name="gl_code"]:not([readonly])');
    
    // Apply integer-only validation to CNIC fields
    cnicInputs.forEach(input => {
        // Set input type to text to allow custom validation
        input.setAttribute('type', 'text');
        
        // Add placeholder
        input.setAttribute('placeholder', 'Numbers only');
        
        // Add input event listener to validate as user types
        input.addEventListener('input', function(e) {
            // Remove any non-numeric characters
            this.value = this.value.replace(/[^0-9]/g, '');
        });
        
        // Add blur event listener for final validation
        input.addEventListener('blur', function(e) {
            if (this.value && !/^\d+$/.test(this.value)) {
                alert('CNIC must contain only numbers.');
                this.value = '';
                this.focus();
            }
        });
    });
    
    // Apply integer-only validation to GL Code fields
    glCodeInputs.forEach(input => {
        // Set input type to text to allow custom validation
        input.setAttribute('type', 'text');
        
        // Add placeholder
        input.setAttribute('placeholder', 'Numbers only');
        
        // Add input event listener to validate as user types
        input.addEventListener('input', function(e) {
            // Remove any non-numeric characters
            this.value = this.value.replace(/[^0-9]/g, '');
        });
        
        // Add blur event listener for final validation
        input.addEventListener('blur', function(e) {
            if (this.value && !/^\d+$/.test(this.value)) {
                alert('GL Code must contain only numbers.');
                this.value = '';
                this.focus();
            }
        });
    });
});