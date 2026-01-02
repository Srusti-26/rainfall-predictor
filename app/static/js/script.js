
// Rainfall Predictor - Dreamy Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('✨ Rainfall Predictor application loaded ✨');
    
    // Create starry background
    createStarryBackground();
    
    // Initialize all components with animations
    initializeComponents();
    
    // Enable all tooltips with custom animation
    initializeTooltips();
    
    // Enhanced form validation
    initializeFormValidation();
    
    // Initialize rainfall visualization if on results page
    initializeRainfallVisualization();
    
    // Add page transition effects
    addPageTransitions();
});

// Create magical starry background
function createStarryBackground() {
    const starsContainer = document.createElement('div');
    starsContainer.className = 'stars';
    document.body.appendChild(starsContainer);
    
    // Create stars with random positions and animations
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.width = `${Math.random() * 2 + 1}px`;
        star.style.height = star.style.width;
        star.style.opacity = Math.random() * 0.8 + 0.2;
        star.style.setProperty('--duration', `${3 + Math.random() * 7}s`);
        star.style.setProperty('--delay', `${Math.random() * 5}s`);
        starsContainer.appendChild(star);
    }
    
    // Create constellation lines
    for (let i = 0; i < 15; i++) {
        const line = document.createElement('div');
        line.className = 'constellation-line';
        line.style.left = `${Math.random() * 90 + 5}%`;
        line.style.top = `${Math.random() * 90 + 5}%`;
        line.style.width = `${Math.random() * 100 + 50}px`;
        line.style.transform = `rotate(${Math.random() * 360}deg)`;
        line.style.opacity = Math.random() * 0.1 + 0.05;
        starsContainer.appendChild(line);
    }
}

// Initialize all components with animations
function initializeComponents() {
    // Animate cards on scroll
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
        
        // Add hover effect for cards
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.5)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
        });
    });
    
    // Animate form inputs with floating effect
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
            
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'input-ripple';
            this.parentElement.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 1000);
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });
        
        // Add shimmer effect on hover
        input.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.boxShadow = '0 0 15px rgba(76, 201, 240, 0.3)';
        });
        
        input.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
    
    // Animate buttons with hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            
            // Create shimmer effect
            const shimmer = document.createElement('span');
            shimmer.className = 'btn-shimmer';
            this.appendChild(shimmer);
            
            setTimeout(() => {
                shimmer.remove();
            }, 1000);
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Animate weather icons with floating effect
    const weatherIcons = document.querySelectorAll('.weather-icon');
    weatherIcons.forEach(icon => {
        setInterval(() => {
            icon.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                icon.style.transform = 'translateY(0)';
            }, 1500);
        }, 3000);
    });
}

// Initialize tooltips with custom animation
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            animation: true,
            delay: { show: 100, hide: 100 },
            template: '<div class="tooltip magical-tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        });
    });
}

// Enhanced form validation
function initializeFormValidation() {
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        // Add magical validation styles
        predictionForm.addEventListener('submit', function(event) {
            if (!predictionForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Highlight invalid fields with animation
                const invalidInputs = predictionForm.querySelectorAll(':invalid');
                invalidInputs.forEach(input => {
                    input.classList.add('shake-animation');
                    setTimeout(() => {
                        input.classList.remove('shake-animation');
                    }, 500);
                });
                
                // Scroll to first invalid field
                if (invalidInputs.length > 0) {
                    invalidInputs[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                // Add loading animation when form is valid
                const submitBtn = predictionForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                    submitBtn.disabled = true;
                }
            }
            
            predictionForm.classList.add('was-validated');
        });
        
        // Add event listeners to numeric inputs to ensure valid ranges with visual feedback
        const numericInputs = document.querySelectorAll('input[type="number"]');
        numericInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const value = parseFloat(this.value);
                const min = parseFloat(this.getAttribute('min'));
                const max = parseFloat(this.getAttribute('max'));
                
                if ((min !== null && !isNaN(min) && value < min) || 
                    (max !== null && !isNaN(max) && value > max)) {
                    
                    // Visual feedback for invalid range
                    this.classList.add('pulse-warning');
                    setTimeout(() => {
                        this.classList.remove('pulse-warning');
                    }, 500);
                    
                    // Correct the value
                    if (min !== null && !isNaN(min) && value < min) {
                        this.value = min;
                    }
                    
                    if (max !== null && !isNaN(max) && value > max) {
                        this.value = max;
                    }
                }
            });
        });
        
        // Location input with auto-complete effect
        const locationInput = document.getElementById('location');
        if (locationInput) {
            locationInput.addEventListener('input', function() {
                if (this.value.length > 2) {
                    // Simulate location search with loading effect
                    const loadingIndicator = document.createElement('div');
                    loadingIndicator.className = 'location-loading';
                    loadingIndicator.innerHTML = '<span class="spinner-small"></span>';
                    
                    // Only add if not already present
                    if (!this.parentElement.querySelector('.location-loading')) {
                        this.parentElement.appendChild(loadingIndicator);
                        
                        // Remove after simulated search
                        setTimeout(() => {
                            loadingIndicator.remove();
                        }, 800);
                    }
                }
            });
            
            // Auto-fill weather data when location is selected
            locationInput.addEventListener('change', function() {
                if (this.value.trim() !== '') {
                    fetchWeatherData(this.value).then(data => {
                        populateFormWithWeatherData(data);
                    });
                }
            });
        }
    }
}

// Initialize rainfall visualization on results page
function initializeRainfallVisualization() {
    const rainfallGaugeFill = document.getElementById('rainfall-gauge-fill');
    if (rainfallGaugeFill) {
        // Get rainfall value from the page
        const rainfallValue = parseFloat(document.querySelector('.display-4').textContent);
        
        // Calculate fill percentage (max at 15mm)
        const fillPercentage = Math.min(rainfallValue / 15 * 100, 100);
        
        // Animate the fill with delay for dramatic effect
        setTimeout(() => {
            rainfallGaugeFill.style.height = fillPercentage + '%';
            
            // Add water ripple effect
            setInterval(() => {
                const ripple = document.createElement('div');
                ripple.className = 'water-ripple';
                rainfallGaugeFill.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 2000);
            }, 3000);
        }, 500);
        
        // Animate confidence meter
        setTimeout(() => {
            const confidenceBar = document.querySelector('.confidence-meter .progress-bar');
            if (confidenceBar) {
                const confidenceValue = confidenceBar.getAttribute('aria-valuenow');
                confidenceBar.style.width = confidenceValue + '%';
            }
        }, 800);
        
        // Animate parameter bars with sequential timing
        const parameterBars = document.querySelectorAll('.parameter-info .progress-bar');
        parameterBars.forEach((bar, index) => {
            setTimeout(() => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }, 1000 + (index * 200));
        });
    }
}

// Add page transitions
function addPageTransitions() {
    // Fade in page content
    const mainContent = document.querySelector('.container');
    if (mainContent) {
        mainContent.style.opacity = '0';
        setTimeout(() => {
            mainContent.style.transition = 'opacity 0.8s ease';
            mainContent.style.opacity = '1';
        }, 100);
    }
    
    // Add transition effect to links
    const links = document.querySelectorAll('a:not([target="_blank"])');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't apply to links with specific classes or attributes
            if (this.classList.contains('no-transition') || 
                this.getAttribute('data-bs-toggle') || 
                this.getAttribute('href').startsWith('#')) {
                return;
            }
            
            e.preventDefault();
            const href = this.getAttribute('href');
            
            // Fade out current page
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease';
            
            // Navigate after transition
            setTimeout(() => {
                window.location.href = href;
            }, 500);
        });
    });
}

// Enhanced function to fetch weather data for a location
async function fetchWeatherData(location) {
    console.log(`✨ Fetching weather data for ${location} ✨`);
    
    // Show loading indicator
    const loadingToast = createToast(`Fetching weather data for ${location}...`);
    document.body.appendChild(loadingToast);
    
    // Simulate API call with delay
    return new Promise((resolve) => {
        setTimeout(() => {
            // Remove loading toast
            loadingToast.classList.add('toast-hide');
            setTimeout(() => loadingToast.remove(), 500);
            
            // Create success toast
            const successToast = createToast(`Weather data loaded for ${location}`, 'success');
            document.body.appendChild(successToast);
            setTimeout(() => {
                successToast.classList.add('toast-hide');
                setTimeout(() => successToast.remove(), 500);
            }, 3000);
            
            // Return simulated data based on location name
            // This creates somewhat realistic data based on the location string
            const locationSum = location.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
            const seed = locationSum / 1000;
            
            resolve({
                temperature: Math.round((seed * 30 + 5) * 10) / 10,
                humidity: Math.round(seed * 60 + 30),
                pressure: Math.round((seed * 50 + 990) * 10) / 10,
                wind_speed: Math.round((seed * 20 + 2) * 10) / 10,
                cloud_cover: Math.round(seed * 80 + 10)
            });
        }, 1200);
    });
}

// Create toast notification
function createToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `magical-toast toast-${type}`;
    
    let icon = '✨';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    if (type === 'warning') icon = '⚠️';
    
    toast.innerHTML = `
        <div class="toast-icon">${icon}</div>
        <div class="toast-message">${message}</div>
    `;
    
    return toast;
}

// Enhanced function to populate the form with weather data
function populateFormWithWeatherData(data) {
    // Get all form fields
    const fields = [
        { id: 'temperature', value: data.temperature },
        { id: 'humidity', value: data.humidity },
        { id: 'pressure', value: data.pressure },
        { id: 'wind_speed', value: data.wind_speed },
        { id: 'cloud_cover', value: data.cloud_cover }
    ];
    
    // Populate each field with animation
    fields.forEach((field, index) => {
        const element = document.getElementById(field.id);
        if (element) {
            // Highlight field before changing
            element.classList.add('highlight-field');
            
            // Set value with delay for sequential effect
            setTimeout(() => {
                // Animate counting up to the value
                const startValue = parseFloat(element.value) || 0;
                const endValue = field.value;
                const duration = 1000; // ms
                const steps = 20;
                const increment = (endValue - startValue) / steps;
                
                let currentStep = 0;
                const animateValue = setInterval(() => {
                    currentStep++;
                    const currentValue = startValue + (increment * currentStep);
                    element.value = Math.round(currentValue * 10) / 10;
                    
                    if (currentStep >= steps) {
                        clearInterval(animateValue);
                        element.value = endValue;
                        element.classList.remove('highlight-field');
                    }
                }, duration / steps);
            }, 300 + (index * 200));
        }
    });
    
    // Suggest season and time of day based on temperature
    setTimeout(() => {
        const seasonSelect = document.getElementById('season');
        const timeSelect = document.getElementById('time_of_day');
        
        if (seasonSelect) {
            let suggestedSeason;
            if (data.temperature > 25) suggestedSeason = 'summer';
            else if (data.temperature > 15) suggestedSeason = 'spring';
            else if (data.temperature > 5) suggestedSeason = 'autumn';
            else suggestedSeason = 'winter';
            
            seasonSelect.value = suggestedSeason;
            seasonSelect.classList.add('highlight-field');
            setTimeout(() => seasonSelect.classList.remove('highlight-field'), 1000);
        }
        
        if (timeSelect) {
            // Suggest a random time of day
            const times = ['morning', 'afternoon', 'evening', 'night'];
            const suggestedTime = times[Math.floor(Math.random() * times.length)];
            
            timeSelect.value = suggestedTime;
            timeSelect.classList.add('highlight-field');
            setTimeout(() => timeSelect.classList.remove('highlight-field'), 1000);
        }
    }, 2000);
}

// Add CSS for JavaScript-specific animations
const styleElement = document.createElement('style');
styleElement.textContent = `
    /* Star and constellation styles */
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        opacity: 0;
        animation: twinkle var(--duration) linear var(--delay) infinite;
    }
    
    .constellation-line {
        position: absolute;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    }
    
    @keyframes twinkle {
        0% { opacity: 0; transform: translateY(0); }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { opacity: 0; transform: translateY(-20px); }
    }
    
    /* Form animations */
    .input-focused {
        transform: translateY(-3px);
    }
    
    .input-ripple {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(76, 201, 240, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: ripple 1s linear forwards;
    }
    
    @keyframes ripple {
        0% { width: 0; height: 0; opacity: 1; }
        100% { width: 200px; height: 200px; opacity: 0; }
    }
    
    .btn-shimmer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmerButton 1s linear forwards;
    }
    
    @keyframes shimmerButton {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Validation animations */
    .shake-animation {
        animation: shake 0.5s linear;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .pulse-warning {
        animation: pulseWarning 0.5s linear;
    }
    
    @keyframes pulseWarning {
        0%, 100% { box-shadow: 0 0 0 rgba(251, 146, 60, 0); }
        50% { box-shadow: 0 0 15px rgba(251, 146, 60, 0.8); }
    }
    
    /* Loading animations */
    .spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    .spinner-small {
        display: inline-block;
        width: 12px;
        height: 12px;
        border: 2px solid rgba(76, 201, 240, 0.3);
        border-radius: 50%;
        border-top-color: #4cc9f0;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .location-loading {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
    }
    
    /* Water effects */
    .water-ripple {
        position: absolute;
        bottom: 50%;
        left: 50%;
        width: 6px;
        height: 6px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        transform: translate(-50%, 50%);
        animation: waterRipple 2s linear forwards;
    }
    
    @keyframes waterRipple {
        0% { width: 0; height: 0; opacity: 1; }
        100% { width: 50px; height: 50px; opacity: 0; }
    }
    
    /* Toast notifications */
    .magical-toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: flex;
        align-items: center;
        padding: 12px 20px;
        background: rgba(30, 41, 59, 0.9);
        backdrop-filter: blur(10px);
        border-left: 4px solid #4cc9f0;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        transform: translateY(0);
        opacity: 1;
        transition: transform 0.5s ease, opacity 0.5s ease;
    }
    
    .magical-toast.toast-success {
        border-left-color: #4ade80;
    }
    
    .magical-toast.toast-error {
        border-left-color: #f87171;
    }
    
    .magical-toast.toast-warning {
        border-left-color: #fbbf24;
    }
    
    .magical-toast.toast-hide {
        transform: translateY(30px);
        opacity: 0;
    }
    
    .toast-icon {
        margin-right: 12px;
        font-size: 18px;
    }
    
    .toast-message {
        color: white;
        font-weight: 500;
    }
    
    /* Field highlight effect */
    .highlight-field {
        animation: highlightPulse 1s ease;
    }
    
    @keyframes highlightPulse {
        0%, 100% { box-shadow: 0 0 0 rgba(76, 201, 240, 0); }
        50% { box-shadow: 0 0 15px rgba(76, 201, 240, 0.8); }
    }
`;

document.head.appendChild(styleElement);
