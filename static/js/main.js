// main.js - Common functionality across all tools

document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Make the header/navbar sticky on scroll
    const header = document.querySelector('.main-header');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Initialize AOS animations if the library is loaded
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }

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

    // Common functions for showing/hiding containers
    window.showProgressContainer = function() {
        if (document.getElementById('progress-container')) {
            document.getElementById('progress-container').style.display = 'block';
        }
        
        if (document.getElementById('url-form-container')) {
            document.getElementById('url-form-container').style.display = 'none';
        }
        
        if (document.getElementById('upload-form-container')) {
            document.getElementById('upload-form-container').style.display = 'none';
        }
        
        if (document.getElementById('data-form-container')) {
            document.getElementById('data-form-container').style.display = 'none';
        }
        
        if (document.getElementById('result-container')) {
            document.getElementById('result-container').style.display = 'none';
        }
        
        if (document.getElementById('error-container')) {
            document.getElementById('error-container').style.display = 'none';
        }
        
        // Update step indicators
        updateStepIndicator(2);
    };

    window.showResultContainer = function() {
        if (document.getElementById('progress-container')) {
            document.getElementById('progress-container').style.display = 'none';
        }
        
        if (document.getElementById('url-form-container')) {
            document.getElementById('url-form-container').style.display = 'none';
        }
        
        if (document.getElementById('upload-form-container')) {
            document.getElementById('upload-form-container').style.display = 'none';
        }
        
        if (document.getElementById('data-form-container')) {
            document.getElementById('data-form-container').style.display = 'none';
        }
        
        if (document.getElementById('result-container')) {
            document.getElementById('result-container').style.display = 'block';
        }
        
        if (document.getElementById('error-container')) {
            document.getElementById('error-container').style.display = 'none';
        }
        
        // Update step indicators
        updateStepIndicator(3);
    };

    window.showErrorContainer = function(errorMessage) {
        if (document.getElementById('progress-container')) {
            document.getElementById('progress-container').style.display = 'none';
        }
        
        if (document.getElementById('result-container')) {
            document.getElementById('result-container').style.display = 'none';
        }
        
        if (document.getElementById('error-container')) {
            document.getElementById('error-container').style.display = 'block';
        }
        
        // Set error message
        if (document.getElementById('error-message')) {
            document.getElementById('error-message').textContent = errorMessage;
        }
        
        // Reset step indicators
        updateStepIndicator(1);
    };

    window.resetFormContainer = function() {
        if (document.getElementById('progress-container')) {
            document.getElementById('progress-container').style.display = 'none';
        }
        
        if (document.getElementById('result-container')) {
            document.getElementById('result-container').style.display = 'none';
        }
        
        if (document.getElementById('error-container')) {
            document.getElementById('error-container').style.display = 'none';
        }
        
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

    // Add click event listeners to common buttons
    const tryAgainBtn = document.getElementById('try-again-btn');
    if (tryAgainBtn) {
        tryAgainBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

    const downloadAnotherBtn = document.getElementById('download-another-btn');
    if (downloadAnotherBtn) {
        downloadAnotherBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

    const convertAnotherBtn = document.getElementById('convert-another-btn');
    if (convertAnotherBtn) {
        convertAnotherBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

    const mergeAnotherBtn = document.getElementById('merge-another-btn');
    if (mergeAnotherBtn) {
        mergeAnotherBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

    const resizeAnotherBtn = document.getElementById('resize-another-btn');
    if (resizeAnotherBtn) {
        resizeAnotherBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

    const generateAnotherBtn = document.getElementById('generate-another-btn');
    if (generateAnotherBtn) {
        generateAnotherBtn.addEventListener('click', function() {
            window.resetFormContainer();
        });
    }

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
