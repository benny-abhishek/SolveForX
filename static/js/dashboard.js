/**
 * Caterpillar Smart Operator Assistant - Dashboard JavaScript
 * Handles real-time updates, charts, and interactive functionality
 */

// Global variables
let realTimeUpdateInterval;
let alertCount = 0;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    startRealTimeUpdates();
    setupEventListeners();
});

/**
 * Initialize dashboard components
 */
function initializeDashboard() {
    console.log('Initializing dashboard...');
    
    // Update alert counters
    updateAlertCounters();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup auto-refresh indicators
    setupRefreshIndicators();
    
    console.log('Dashboard initialized successfully');
}

/**
 * Start real-time data updates
 */
function startRealTimeUpdates() {
    // Update every 30 seconds
    realTimeUpdateInterval = setInterval(function() {
        updateDashboardData();
        updateSystemStatus();
    }, 30000);
    
    console.log('Real-time updates started');
}

/**
 * Update dashboard data via simulated real-time updates
 */
function updateDashboardData() {
    try {
        // Simulate real-time safety score updates
        updateSafetyScore();
        
        // Update machine status indicators
        updateMachineStatus();
        
        // Refresh task counters
        updateTaskCounters();
        
        // Update last refresh time
        updateLastRefreshTime();
        
    } catch (error) {
        console.error('Error updating dashboard data:', error);
        showNotification('Warning: Data update failed. Retrying...', 'warning');
    }
}

/**
 * Update safety score with animation
 */
function updateSafetyScore() {
    const safetyScoreElement = document.querySelector('.stat-card .text-white h2');
    if (safetyScoreElement && safetyScoreElement.textContent.includes('%')) {
        const currentScore = parseFloat(safetyScoreElement.textContent);
        // Simulate slight variations in safety score
        const variation = (Math.random() - 0.5) * 2; // +/- 1%
        const newScore = Math.max(85, Math.min(100, currentScore + variation));
        
        animateNumber(safetyScoreElement, currentScore, newScore, '%');
    }
}

/**
 * Update machine status indicators
 */
function updateMachineStatus() {
    const machineCards = document.querySelectorAll('.machine-status-card');
    machineCards.forEach(card => {
        // Simulate status changes (very low probability)
        if (Math.random() < 0.05) { // 5% chance of status change
            const statusClasses = ['status-safe', 'status-warning', 'status-danger'];
            const currentStatus = statusClasses.find(cls => card.classList.contains(cls));
            
            if (currentStatus) {
                card.classList.remove(currentStatus);
                // Bias towards safe status
                const newStatus = Math.random() < 0.7 ? 'status-safe' : 
                                 Math.random() < 0.9 ? 'status-warning' : 'status-danger';
                card.classList.add(newStatus);
                
                // Update status indicator
                const indicator = card.querySelector('.status-indicator');
                if (indicator) {
                    indicator.className = `status-indicator ${newStatus}`;
                }
            }
        }
    });
}

/**
 * Update task counters
 */
function updateTaskCounters() {
    // This would normally fetch real data from the server
    // For now, we'll simulate minor changes
    const taskCountElement = document.querySelector('.bg-gradient-warning h2');
    if (taskCountElement) {
        const currentCount = parseInt(taskCountElement.textContent);
        // Simulate task completion (slight decrease)
        if (Math.random() < 0.1) { // 10% chance
            const newCount = Math.max(0, currentCount - 1);
            animateNumber(taskCountElement, currentCount, newCount);
        }
    }
}

/**
 * Animate number changes
 */
function animateNumber(element, startValue, endValue, suffix = '') {
    const duration = 1000; // 1 second
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentValue = startValue + (endValue - startValue) * easeOut;
        
        element.textContent = Math.round(currentValue * 10) / 10 + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

/**
 * Update system status indicator
 */
function updateSystemStatus() {
    const statusElement = document.getElementById('system-status');
    if (statusElement) {
        // Simulate system health check
        const isHealthy = Math.random() > 0.05; // 95% uptime
        statusElement.className = isHealthy ? 'text-success' : 'text-warning';
        statusElement.innerHTML = isHealthy ? 
            '<i class="fas fa-check-circle me-1"></i>All Systems Operational' :
            '<i class="fas fa-exclamation-triangle me-1"></i>Minor Issues Detected';
    }
}

/**
 * Update alert counters
 */
function updateAlertCounters() {
    const alertElements = document.querySelectorAll('.alert-count');
    alertElements.forEach(element => {
        alertCount++;
        element.textContent = alertCount;
    });
}

/**
 * Update last refresh time
 */
function updateLastRefreshTime() {
    const refreshElements = document.querySelectorAll('.last-refresh');
    refreshElements.forEach(element => {
        element.textContent = new Date().toLocaleTimeString();
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Incident report form validation
    const incidentForm = document.querySelector('#reportIncidentModal form');
    if (incidentForm) {
        incidentForm.addEventListener('submit', validateIncidentForm);
    }
    
    // Quick action buttons
    setupQuickActionButtons();
    
    // Refresh button
    const refreshButton = document.getElementById('refresh-dashboard');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            showLoadingState(true);
            updateDashboardData();
            setTimeout(() => showLoadingState(false), 1000);
        });
    }
    
    // Auto-refresh toggle
    const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('change', function() {
            if (this.checked) {
                startRealTimeUpdates();
            } else {
                clearInterval(realTimeUpdateInterval);
            }
        });
    }
}

/**
 * Setup quick action buttons
 */
function setupQuickActionButtons() {
    const quickActionButtons = document.querySelectorAll('.btn[href]');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state to buttons
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            this.disabled = true;
            
            // Restore button after short delay (simulating navigation)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 500);
        });
    });
}

/**
 * Validate incident report form
 */
function validateIncidentForm(event) {
    event.preventDefault();
    
    const form = event.target;
    const machineId = form.querySelector('#machine_id').value;
    const operatorId = form.querySelector('#operator_id').value;
    const incidentType = form.querySelector('#incident_type').value;
    const severity = form.querySelector('#severity').value;
    const description = form.querySelector('#description').value;
    
    // Clear previous errors
    clearFormErrors(form);
    
    let isValid = true;
    
    // Validate required fields
    if (!machineId) {
        showFieldError(form, 'machine_id', 'Please select a machine');
        isValid = false;
    }
    
    if (!operatorId) {
        showFieldError(form, 'operator_id', 'Please select an operator');
        isValid = false;
    }
    
    if (!incidentType) {
        showFieldError(form, 'incident_type', 'Please select an incident type');
        isValid = false;
    }
    
    if (!severity) {
        showFieldError(form, 'severity', 'Please select severity level');
        isValid = false;
    }
    
    if (!description || description.trim().length < 10) {
        showFieldError(form, 'description', 'Please provide a detailed description (minimum 10 characters)');
        isValid = false;
    }
    
    if (isValid) {
        // Show confirmation dialog
        if (confirm('Submit this safety incident report?')) {
            submitIncidentReport(form);
        }
    }
}

/**
 * Submit incident report
 */
function submitIncidentReport(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
    submitButton.disabled = true;
    
    // Simulate form submission delay
    setTimeout(() => {
        form.submit();
        showNotification('Incident report submitted successfully', 'success');
    }, 1000);
}

/**
 * Show field error
 */
function showFieldError(form, fieldName, message) {
    const field = form.querySelector(`#${fieldName}`);
    if (field) {
        field.classList.add('is-invalid');
        
        // Create or update error message
        let errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            field.parentNode.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }
}

/**
 * Clear form errors
 */
function clearFormErrors(form) {
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
    form.querySelectorAll('.invalid-feedback').forEach(error => {
        error.remove();
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup refresh indicators
 */
function setupRefreshIndicators() {
    // Add refresh indicator to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const header = card.querySelector('.card-header');
        if (header) {
            const refreshIcon = document.createElement('i');
            refreshIcon.className = 'fas fa-sync-alt text-muted float-end refresh-icon';
            refreshIcon.style.cursor = 'pointer';
            refreshIcon.title = 'Last updated: ' + new Date().toLocaleTimeString();
            header.appendChild(refreshIcon);
            
            refreshIcon.addEventListener('click', function() {
                this.style.animation = 'spin 1s linear';
                setTimeout(() => {
                    this.style.animation = '';
                    this.title = 'Last updated: ' + new Date().toLocaleTimeString();
                }, 1000);
            });
        }
    });
}

/**
 * Show loading state
 */
function showLoadingState(show) {
    const dashboard = document.querySelector('main');
    if (show) {
        dashboard.classList.add('loading');
    } else {
        dashboard.classList.remove('loading');
    }
}

/**
 * View incident details
 */
function viewIncident(incidentId) {
    console.log('Viewing incident:', incidentId);
    // This function is called from the template
    // Implementation would typically fetch and display incident details
}

/**
 * Cleanup on page unload
 */
window.addEventListener('beforeunload', function() {
    if (realTimeUpdateInterval) {
        clearInterval(realTimeUpdateInterval);
    }
});

// Export functions for use in templates
window.dashboardFunctions = {
    viewIncident,
    showNotification,
    updateDashboardData
};
