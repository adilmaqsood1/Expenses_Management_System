/**
 * MIS Dashboard JavaScript - Enhanced Version
 * Handles data visualization and filtering for the MIS Analytics Dashboard
 * with improved animations, transitions, and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Set default chart colors and styles
    Chart.defaults.font.family = '"Inter", "Helvetica", "Arial", sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(17, 24, 39, 0.8)';
    Chart.defaults.plugins.tooltip.titleColor = '#fff';
    Chart.defaults.plugins.tooltip.bodyColor = '#fff';
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 6;
    Chart.defaults.plugins.tooltip.displayColors = true;
    Chart.defaults.plugins.tooltip.boxPadding = 6;
    Chart.defaults.plugins.tooltip.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.padding = 15;
    Chart.defaults.plugins.legend.title.padding = 10;
    Chart.defaults.plugins.legend.title.font = {
        weight: 'bold'
    };
    
    // Add subtle animation to stats cards
    document.querySelectorAll('.stats-card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-slideInBottom');
    });
    
    // Initialize date pickers with default values
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    if (document.getElementById('start-date')) {
        document.getElementById('start-date').valueAsDate = thirtyDaysAgo;
    }
    
    if (document.getElementById('end-date')) {
        document.getElementById('end-date').valueAsDate = today;
    }
    
    // Handle date range selection
    const dateRangeSelect = document.getElementById('date-range');
    const customDateRange = document.getElementById('custom-date-range');
    
    if (dateRangeSelect) {
        dateRangeSelect.addEventListener('change', function() {
            if (this.value === 'custom') {
                customDateRange.classList.remove('hidden');
            } else {
                customDateRange.classList.add('hidden');
            }
        });
    }
    
    // Handle filter application
    const applyFiltersBtn = document.getElementById('apply-filters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            fetchFilteredData();
        });
    }
    
    /**
     * Fetch filtered data from the server based on selected filters
     */
    function fetchFilteredData() {
        // Get filter values
        const dateRange = document.getElementById('date-range').value;
        let startDate = null;
        let endDate = null;
        
        if (dateRange === 'custom') {
            startDate = document.getElementById('start-date').value;
            endDate = document.getElementById('end-date').value;
        }
        
        const headFilter = document.getElementById('head-filter').value;
        const branchFilter = document.getElementById('branch-filter').value;
        const vendorFilter = document.getElementById('vendor-filter').value;
        const statusFilter = document.getElementById('status-filter').value;
        
        // Show loading state with enhanced animation
        document.querySelectorAll('.chart-container').forEach((container, index) => {
            // Create a modern loading spinner
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.style.animationDelay = `${index * 0.1}s`;
            
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            
            loadingOverlay.appendChild(spinner);
            container.appendChild(loadingOverlay);
            container.classList.add('loading');
        });
        
        // Prepare the data to send
        const filterData = {
            date_range: dateRange,
            start_date: startDate,
            end_date: endDate,
            head: headFilter,
            branch: branchFilter,
            vendor: vendorFilter,
            status: statusFilter
        };
        
        // Make AJAX request to get filtered data
        fetch('/api/mis-dashboard-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(filterData)
        })
        .then(response => response.json())
        .then(data => {
            // Update summary cards
            updateSummaryCards(data.summary);
            
            // Update charts
            updateCharts(data.charts);
            
            // Update top expenses table
            updateTopExpensesTable(data.top_expenses);
            
            // Remove loading state with fade-out animation
            document.querySelectorAll('.chart-container').forEach((container, index) => {
                const loadingOverlay = container.querySelector('.loading-overlay');
                if (loadingOverlay) {
                    // Add fade-out animation
                    loadingOverlay.style.opacity = '0';
                    loadingOverlay.style.transition = 'opacity 0.5s ease';
                    
                    // Remove after animation completes
                    setTimeout(() => {
                        loadingOverlay.remove();
                        container.classList.remove('loading');
                        
                        // Add a subtle scale animation to the chart
                        const canvas = container.querySelector('canvas');
                        if (canvas) {
                            canvas.style.transform = 'scale(0.95)';
                            canvas.style.transition = 'transform 0.3s ease';
                            setTimeout(() => {
                                canvas.style.transform = 'scale(1)';
                            }, 50);
                        }
                    }, 500);
                }
            });
            
            // Show success notification
            showNotification('Data updated successfully', 'success');
        })
        .catch(error => {
            console.error('Error fetching filtered data:', error);
            // Remove loading state with fade-out animation
            document.querySelectorAll('.chart-container').forEach((container, index) => {
                const loadingOverlay = container.querySelector('.loading-overlay');
                if (loadingOverlay) {
                    // Add fade-out animation
                    loadingOverlay.style.opacity = '0';
                    loadingOverlay.style.transition = 'opacity 0.5s ease';
                    
                    // Remove after animation completes
                    setTimeout(() => {
                        loadingOverlay.remove();
                        container.classList.remove('loading');
                        
                        // Add a subtle scale animation to the chart
                        const canvas = container.querySelector('canvas');
                        if (canvas) {
                            canvas.style.transform = 'scale(0.95)';
                            canvas.style.transition = 'transform 0.3s ease';
                            setTimeout(() => {
                                canvas.style.transform = 'scale(1)';
                            }, 50);
                        }
                    }, 500);
                }
            });
            
            // Show error notification instead of alert
            showNotification('An error occurred while fetching data. Please try again.', 'error');
        });
    }
    
    /**
     * Update summary cards with new data
     */
    function updateSummaryCards(summary) {
        if (document.getElementById('total-expenses')) {
            document.getElementById('total-expenses').textContent = '₨ ' + summary.total_expenses.toFixed(2);
        }
        
        if (document.getElementById('avg-expense')) {
            document.getElementById('avg-expense').textContent = '₨ ' + summary.avg_expense.toFixed(2);
        }
        
        if (document.getElementById('expense-count')) {
            document.getElementById('expense-count').textContent = summary.expense_count;
        }
        
        if (document.getElementById('budget-utilization')) {
            const budgetUtilization = document.getElementById('budget-utilization');
            budgetUtilization.textContent = summary.budget_utilization + '%';
            
            // Update the status text
            const statusElement = budgetUtilization.nextElementSibling;
            statusElement.className = 'text-xs mt-1';
            
            if (summary.budget_utilization < 75) {
                statusElement.classList.add('text-blue-500');
                statusElement.textContent = 'On track';
            } else if (summary.budget_utilization < 90) {
                statusElement.classList.add('text-yellow-500');
                statusElement.textContent = 'Caution';
            } else {
                statusElement.classList.add('text-red-500');
                statusElement.textContent = 'Over budget';
            }
        }
    }
    
    /**
     * Update all charts with new data and enhanced animations
     */
    function updateCharts(chartData) {
        // Enhanced chart update options with animations
        const updateOptions = {
            duration: 800,
            easing: 'easeOutQuart',
            responsive: true,
            maintainAspectRatio: false
        };
        
        // Update expense by head chart with enhanced colors
        if (window.expenseByHeadChart) {
            // Generate vibrant colors for pie chart
            const headColors = generateGradientColors(chartData.head_labels.length, [
                [255, 99, 132],   // Red
                [54, 162, 235],   // Blue
                [255, 206, 86],   // Yellow
                [75, 192, 192],   // Teal
                [153, 102, 255],  // Purple
                [255, 159, 64]    // Orange
            ]);
            
            window.expenseByHeadChart.data.labels = chartData.head_labels;
            window.expenseByHeadChart.data.datasets[0].data = chartData.head_values;
            window.expenseByHeadChart.data.datasets[0].backgroundColor = headColors;
            window.expenseByHeadChart.update(updateOptions);
        }
        
        // Update expense trend chart with enhanced styling
        if (window.expenseTrendChart) {
            window.expenseTrendChart.data.labels = chartData.trend_labels;
            window.expenseTrendChart.data.datasets[0].data = chartData.trend_values;
            // Add gradient background
            const ctx = document.getElementById('expense-trend-chart').getContext('2d');
            const gradient = ctx.createLinearGradient(0, 0, 0, 300);
            gradient.addColorStop(0, 'rgba(75, 192, 192, 0.2)');
            gradient.addColorStop(1, 'rgba(75, 192, 192, 0)');
            window.expenseTrendChart.data.datasets[0].backgroundColor = gradient;
            window.expenseTrendChart.data.datasets[0].borderWidth = 3;
            window.expenseTrendChart.update(updateOptions);
        }
        
        // Update expense by branch chart with enhanced colors
        if (window.expenseByBranchChart) {
            // Generate vibrant colors for bar chart
            const branchColors = generateGradientColors(chartData.branch_labels.length, [
                [54, 162, 235],   // Blue
                [75, 192, 192],   // Teal
                [153, 102, 255],  // Purple
                [255, 159, 64],   // Orange
                [255, 99, 132]    // Red
            ]);
            
            window.expenseByBranchChart.data.labels = chartData.branch_labels;
            window.expenseByBranchChart.data.datasets[0].data = chartData.branch_values;
            window.expenseByBranchChart.data.datasets[0].backgroundColor = branchColors;
            window.expenseByBranchChart.update(updateOptions);
        }
        
        // Update expense by status chart with enhanced styling
        if (window.expenseByStatusChart) {
            const statusColors = [
                'rgba(255, 206, 86, 0.8)',  // Pending - Yellow
                'rgba(75, 192, 192, 0.8)',  // Approved - Green
                'rgba(255, 99, 132, 0.8)'   // Rejected - Red
            ];
            
            window.expenseByStatusChart.data.labels = chartData.status_labels;
            window.expenseByStatusChart.data.datasets[0].data = chartData.status_values;
            window.expenseByStatusChart.data.datasets[0].backgroundColor = statusColors;
            window.expenseByStatusChart.update(updateOptions);
        }
        
        // Update top vendors chart with enhanced styling
        if (window.topVendorsChart) {
            // Create gradient colors for each vendor
            const vendorColors = chartData.vendor_labels.map((_, index) => {
                const hue = 210 + (index * 30) % 360; // Blue-based hue rotation
                return `hsla(${hue}, 80%, 60%, 0.8)`;
            });
            
            window.topVendorsChart.data.labels = chartData.vendor_labels;
            window.topVendorsChart.data.datasets[0].data = chartData.vendor_values;
            window.topVendorsChart.data.datasets[0].backgroundColor = vendorColors;
            window.topVendorsChart.update(updateOptions);
        }
        
        // Update monthly comparison chart with enhanced styling
        if (window.monthlyComparisonChart) {
            window.monthlyComparisonChart.data.labels = chartData.monthly_labels;
            window.monthlyComparisonChart.data.datasets[0].data = chartData.current_year_values;
            window.monthlyComparisonChart.data.datasets[1].data = chartData.previous_year_values;
            
            // Enhanced colors with transparency
            window.monthlyComparisonChart.data.datasets[0].backgroundColor = 'rgba(75, 192, 192, 0.7)';
            window.monthlyComparisonChart.data.datasets[1].backgroundColor = 'rgba(153, 102, 255, 0.7)';
            
            // Add border for better visibility
            window.monthlyComparisonChart.data.datasets[0].borderColor = 'rgba(75, 192, 192, 1)';
            window.monthlyComparisonChart.data.datasets[1].borderColor = 'rgba(153, 102, 255, 1)';
            window.monthlyComparisonChart.data.datasets[0].borderWidth = 1;
            window.monthlyComparisonChart.data.datasets[1].borderWidth = 1;
            
            window.monthlyComparisonChart.update(updateOptions);
        }
    }
    
    /**
     * Update top expenses table with new data
     */
    function updateTopExpensesTable(expenses) {
        const tableBody = document.getElementById('top-expenses-table');
        if (!tableBody) return;
        
        // Clear existing rows
        tableBody.innerHTML = '';
        
        if (expenses.length === 0) {
            // No expenses found
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">No expenses found</td>
            `;
            tableBody.appendChild(row);
            return;
        }
        
        // Add new rows
        expenses.forEach(expense => {
            const row = document.createElement('tr');
            
            // Format date
            const date = new Date(expense.invoice_date);
            const formattedDate = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
            
            // Determine status class
            let statusClass = '';
            if (expense.status === 'Approved') {
                statusClass = 'bg-green-100 text-green-800';
            } else if (expense.status === 'Pending') {
                statusClass = 'bg-yellow-100 text-yellow-800';
            } else {
                statusClass = 'bg-red-100 text-red-800';
            }
            
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${expense.invoice_no}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${expense.head_name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${expense.vendor_name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${formattedDate}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">₨ ${expense.amount.toFixed(2)}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                        ${expense.status}
                    </span>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }
    
    /**
     * Helper function to get CSRF token from cookies
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Add notification container to the page
    const notificationContainer = document.createElement('div');
    notificationContainer.className = 'notification-container';
    document.body.appendChild(notificationContainer);
    
    // Add enhanced styles for notifications and loading indicators
    const style = document.createElement('style');
    style.textContent = `
        .chart-container.loading {
            position: relative;
        }
        
        .loading-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(4px);
            z-index: 10;
            border-radius: 8px;
        }
        
        .loading-spinner {
            position: relative;
            width: 40px;
            height: 40px;
        }
        
        .loading-spinner::before,
        .loading-spinner::after {
            content: '';
            position: absolute;
            border-radius: 50%;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .loading-spinner::before {
            border: 3px solid rgba(59, 130, 246, 0.2);
        }
        
        .loading-spinner::after {
            border: 3px solid transparent;
            border-top-color: #3b82f6;
            animation: spin 1s cubic-bezier(0.6, 0.2, 0.4, 0.8) infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .notification-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .notification {
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            min-width: 300px;
            transform: translateX(120%);
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(8px);
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification-success {
            background: linear-gradient(to right, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9));
            color: white;
            border-left: 4px solid #059669;
        }
        
        .notification-error {
            background: linear-gradient(to right, rgba(239, 68, 68, 0.9), rgba(220, 38, 38, 0.9));
            color: white;
            border-left: 4px solid #dc2626;
        }
        
        .notification-info {
            background: linear-gradient(to right, rgba(59, 130, 246, 0.9), rgba(37, 99, 235, 0.9));
            color: white;
            border-left: 4px solid #2563eb;
        }
        
        .notification-icon {
            margin-right: 12px;
            font-size: 20px;
        }
        
        .notification-message {
            flex-grow: 1;
            font-weight: 500;
        }
        
        .notification-close {
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
            font-size: 18px;
            margin-left: 8px;
        }
        
        .notification-close:hover {
            opacity: 1;
        }
        
        @media (prefers-color-scheme: dark) {
            .loading-overlay {
                background-color: rgba(17, 24, 39, 0.9);
            }
            
            .loading-spinner::before {
                border-color: rgba(59, 130, 246, 0.3);
            }
        }
    `;
    document.head.appendChild(style);
    
    /**
     * Show a notification message
     * @param {string} message - The message to display
     * @param {string} type - The type of notification (success, error, info)
     */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        // Icon based on notification type
        let icon = '🔔';
        if (type === 'success') icon = '✅';
        if (type === 'error') icon = '❌';
        
        notification.innerHTML = `
            <span class="notification-icon">${icon}</span>
            <span class="notification-message">${message}</span>
            <span class="notification-close">×</span>
        `;
        
        notificationContainer.appendChild(notification);
        
        // Trigger animation
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Add click event to close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.style.transform = 'translateX(120%)';
            setTimeout(() => notification.remove(), 300);
        });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.transform = 'translateX(120%)';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }
    
    /**
     * Generate an array of gradient colors
     * @param {number} count - Number of colors to generate
     * @param {Array} baseColors - Array of base RGB color arrays
     * @returns {Array} Array of color strings
     */
    function generateGradientColors(count, baseColors) {
        const colors = [];
        
        for (let i = 0; i < count; i++) {
            // Use modulo to cycle through base colors
            const baseColor = baseColors[i % baseColors.length];
            
            // Slightly vary the color to create visual interest
            const r = Math.max(0, Math.min(255, baseColor[0] + (Math.random() * 20 - 10)));
            const g = Math.max(0, Math.min(255, baseColor[1] + (Math.random() * 20 - 10)));
            const b = Math.max(0, Math.min(255, baseColor[2] + (Math.random() * 20 - 10)));
            
            colors.push(`rgba(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}, 0.8)`);
        }
        
        return colors;
    }
});