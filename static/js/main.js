// main.js - Common functionality across all tools

document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation initialization
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Common functions for showing/hiding containers
    window.showProgressContainer = function() {
        document.getElementById('progress-container').style.display = 'block';
        document.getElementById('url-form-container')?.style.display = 'none';
        document.getElementById('upload-form-container')?.style.display = 'none';
        document.getElementById('data-form-container')?.style.display = 'none';
        document.getElementById('result-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'none';
        
        // Update step indicators
        updateStepIndicator(2);
    };

    window.showResultContainer = function() {
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('url-form-container')?.style.display = 'none';
        document.getElementById('upload-form-container')?.style.display = 'none';
        document.getElementById('data-form-container')?.style.display = 'none';
        document.getElementById('result-container').style.display = 'block';
        document.getElementById('error-container').style.display = 'none';
        
        // Update step indicators
        updateStepIndicator(3);
    };

    window.showErrorContainer = function(errorMessage) {
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('result-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'block';
        
        // Set error message
        document.getElementById('error-message').textContent = errorMessage;
        
        // Reset step indicators
        updateStepIndicator(1);
    };

    window.resetFormContainer = function() {
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('result-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'none';
        
        // Show the appropriate form container based on what's available
        if (document.getElementById('url-form-container')) {
            document.getElementById('url-form-container').style.display = 'block';
        } else if (document.getElementById('upload-form-container')) {
            document.getElementById('upload-form-container').style.display = 'block';
        } else if (document.getElementById('data-form-container')) {
            document.getElementById('data-form-container').style.display = 'block';
        }
        
        // Reset form validation
        const form = document.querySelector('.needs-validation');
        if (form) {
            form.classList.remove('was-validated');
            form.reset();
        }
        
        // Reset step indicators
        updateStepIndicator(1);
    };

    // Function to update step indicators
    function updateStepIndicator(activeStep) {
        const steps = document.querySelectorAll('.step-indicator .step');
        if (steps.length === 0) return;
        
        steps.forEach((step, index) => {
            if (index + 1 === activeStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    // Add click event listeners to common buttons
    document.getElementById('try-again-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    document.getElementById('download-another-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    document.getElementById('convert-another-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    document.getElementById('merge-another-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    document.getElementById('resize-another-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    document.getElementById('generate-another-btn')?.addEventListener('click', function() {
        window.resetFormContainer();
    });

    // Humanize file size
    window.humanFileSize = function(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    };
});
