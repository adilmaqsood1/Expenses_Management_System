// Main JavaScript file for the expense management system

document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const currentPath = window.location.pathname;
    
    // Find all nav items
    const navItems = document.querySelectorAll('.nav-item');
    
    // Add click effect
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Add a ripple effect when clicked
            const ripple = document.createElement('span');
            ripple.classList.add('nav-ripple');
            this.appendChild(ripple);
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});