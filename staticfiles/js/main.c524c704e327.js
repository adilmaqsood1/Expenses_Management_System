// Main JavaScript file for the expense management system

document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const currentPath = window.location.pathname;
    
    // Find all nav items
    const navItems = document.querySelectorAll('.nav-item');
    
    // Add click effect and highlight active nav item
    navItems.forEach(item => {
        // Add ripple effect on click
        item.addEventListener('click', function(e) {
            // Create ripple element at click position
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('nav-ripple');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            this.appendChild(ripple);
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
        
        // Check if this nav item corresponds to current page
        const href = item.getAttribute('href');
        if (href && (currentPath === href || currentPath.includes(href.split('/')[1]))) {
            item.classList.add('active');
        }
    });
    
    // Add responsive menu toggle for mobile
    const header = document.querySelector('.header');
    if (header) {
        const menuToggle = document.createElement('button');
        menuToggle.classList.add('menu-toggle', 'hidden', 'md:hidden');
        menuToggle.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
            </svg>
        `;
        header.appendChild(menuToggle);
        
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu) {
            menuToggle.addEventListener('click', function() {
                navMenu.classList.toggle('mobile-open');
            });
        }
    }
});