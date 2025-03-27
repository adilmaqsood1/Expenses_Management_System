// GL Code conversion script for expense management system 
// Function to convert regular limit to millions

document.addEventListener('DOMContentLoaded', function() {
    // Get the limit and limit_in_millions input fields
    const limitInput = document.getElementById('limit');
    const limitInMillionsInput = document.getElementById('limit_in_millions');
    
    // Only proceed if we're on a page with these fields
    if (limitInput && limitInMillionsInput) {
        // Function to convert regular limit to millions
        function convertToMillions(value) {
            if (!value) return '';
            return (parseFloat(value) / 1000000).toFixed(3);
        }
        
        // Function to convert millions to regular limit
        function convertFromMillions(value) {
            if (!value) return '';
            return (parseFloat(value) * 1000000).toFixed(2);
        }
        
        // Add event listener for the limit field
        limitInput.addEventListener('input', function() {
            // Prevent infinite loop by only updating if this field has focus
            if (document.activeElement === this && this.value) {
                limitInMillionsInput.value = convertToMillions(this.value);
            }
        });
        
        // Add event listener for the limit_in_millions field
        limitInMillionsInput.addEventListener('input', function() {
            // Prevent infinite loop by only updating if this field has focus
            if (document.activeElement === this && this.value) {
                limitInput.value = convertFromMillions(this.value);
            }
        });
    }
});


// done 