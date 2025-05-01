/**
 * Enhanced Login Page JavaScript
 * Adds animations and interactive elements to the login page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add particle animation to background
    function createParticles() {
        const container = document.querySelector('.login-bg-pattern .pattern-grid');
        if (!container) return;
        
        // Clear existing particles
        container.innerHTML = '';
        
        // Create new particles with varying sizes and animation delays
        for (let i = 0; i < 100; i++) {
            const particle = document.createElement('div');
            particle.className = 'pattern-item';
            
            // Randomize size
            const size = Math.floor(Math.random() * 80) + 40; // 40px to 120px
            particle.style.height = `${size}px`;
            particle.style.width = `${size}px`;
            
            // Randomize animation delay
            const delay = Math.random() * 8;
            particle.style.animationDelay = `${delay}s`;
            
            // Randomize opacity
            const opacity = (Math.random() * 0.5) + 0.2; // 0.2 to 0.7
            particle.style.opacity = opacity;
            
            container.appendChild(particle);
        }
    }
    
    // Add subtle hover effects to form inputs
    function enhanceFormInputs() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
        inputs.forEach(input => {
            // Add focus effect
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('input-focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('input-focused');
            });
            
            // Add label animation
            const label = input.previousElementSibling;
            if (label && label.tagName === 'LABEL') {
                input.addEventListener('focus', function() {
                    label.classList.add('label-active');
                });
                
                input.addEventListener('blur', function() {
                    if (!this.value) {
                        label.classList.remove('label-active');
                    }
                });
                
                // Check if input has value on page load
                if (input.value) {
                    label.classList.add('label-active');
                }
            }
        });
    }
    
    // Add ripple effect to login button
    function addButtonRippleEffect() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const ripple = document.createElement('span');
                ripple.classList.add('btn-ripple');
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // Initialize all enhancements
    createParticles();
    enhanceFormInputs();
    addButtonRippleEffect();
    
    // Add subtle animation to the login container on load
    const loginContainer = document.querySelector('.login-container');
    if (loginContainer) {
        loginContainer.classList.add('animate-in');
    }
});