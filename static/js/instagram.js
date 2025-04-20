// instagram.js - Handles Instagram reel downloading functionality

document.addEventListener('DOMContentLoaded', function() {
    // Instagram Downloader Form
    const instagramForm = document.getElementById('instagram-form');
    if (instagramForm) {
        instagramForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity()) {
                this.classList.add('was-validated');
                return;
            }
            
            const postUrl = document.getElementById('post-url').value;
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            formData.append('post_url', postUrl);
            
            // Make AJAX request to the server
            fetch('/api/instagram-download', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Set download link
                    const downloadLink = document.getElementById('download-link');
                    downloadLink.href = data.download_url;
                    
                    // Show result container
                    window.showResultContainer();
                } else {
                    // Show error message
                    window.showErrorContainer(data.error || "An error occurred while downloading the Instagram reel.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
    
    // Helper function to validate Instagram URLs
    function isValidInstagramUrl(url) {
        // Basic Instagram URL validation
        const regex = /^https?:\/\/(www\.)?instagram\.com\/(p|reel|tv)\/[\w-]+\/?/;
        return regex.test(url);
    }
    
    // URL validation for Instagram
    const postUrlInput = document.getElementById('post-url');
    if (postUrlInput) {
        postUrlInput.addEventListener('input', function() {
            if (this.value && !isValidInstagramUrl(this.value)) {
                this.setCustomValidity('Please enter a valid Instagram post URL');
            } else {
                this.setCustomValidity('');
            }
        });
    }
});
