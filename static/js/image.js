// image.js - Handles image resizing functionality

document.addEventListener('DOMContentLoaded', function() {
    // Image Resizer Form
    const imageResizeForm = document.getElementById('image-resize-form');
    if (imageResizeForm) {
        const imageInput = document.getElementById('image-file');
        const imagePreviewContainer = document.getElementById('image-preview-container');
        const imagePreview = document.getElementById('image-preview');
        const originalDimensions = document.getElementById('original-dimensions');
        const fileSize = document.getElementById('file-size');
        const widthInput = document.getElementById('width');
        const heightInput = document.getElementById('height');
        const maintainAspectRatio = document.getElementById('maintain-aspect-ratio');
        const resizeBtn = document.getElementById('resize-btn');
        const dimensionsContainer = document.getElementById('dimensions-container');
        
        // Original image dimensions
        let imgWidth = 0;
        let imgHeight = 0;
        let aspectRatio = 1;
        
        // File selection change handler
        imageInput.addEventListener('change', function(event) {
            if (!event.target.files.length) {
                imagePreviewContainer.style.display = 'none';
                dimensionsContainer.style.display = 'none';
                resizeBtn.disabled = true;
                return;
            }
            
            const file = event.target.files[0];
            
            // Check file size (max 10MB)
            if (file.size > 10 * 1024 * 1024) {
                alert('File size exceeds the 10MB limit.');
                imageInput.value = '';
                return;
            }
            
            // Create preview
            const reader = new FileReader();
            reader.onload = function(e) {
                // Create an image object to get dimensions
                const img = new Image();
                img.onload = function() {
                    imgWidth = img.width;
                    imgHeight = img.height;
                    aspectRatio = imgWidth / imgHeight;
                    
                    // Set original dimensions
                    originalDimensions.textContent = `${imgWidth} x ${imgHeight}`;
                    
                    // Set initial resize dimensions
                    widthInput.value = imgWidth;
                    heightInput.value = imgHeight;
                    
                    // Display preview and dimensions
                    imagePreview.src = e.target.result;
                    imagePreviewContainer.style.display = 'block';
                    dimensionsContainer.style.display = 'block';
                    fileSize.textContent = window.humanFileSize(file.size);
                    resizeBtn.disabled = false;
                };
                img.src = e.target.result;
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
        
        // Maintain aspect ratio functionality
        widthInput.addEventListener('input', function() {
            if (maintainAspectRatio.checked && this.value > 0) {
                heightInput.value = Math.round(this.value / aspectRatio);
            }
        });
        
        heightInput.addEventListener('input', function() {
            if (maintainAspectRatio.checked && this.value > 0) {
                widthInput.value = Math.round(this.value * aspectRatio);
            }
        });
        
        // Form submit handler
        imageResizeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity()) {
                this.classList.add('was-validated');
                return;
            }
            
            const width = parseInt(widthInput.value);
            const height = parseInt(heightInput.value);
            
            // Validate dimensions
            if (width <= 0 || height <= 0 || width > 10000 || height > 10000) {
                alert('Please enter valid dimensions (between 1 and 10000 pixels).');
                return;
            }
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);
            formData.append('width', width);
            formData.append('height', height);
            
            // Make AJAX request to the server
            fetch('/api/resize-image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Set download link
                    const downloadLink = document.getElementById('download-link');
                    downloadLink.href = data.download_url;
                    
                    // Set new dimensions
                    document.getElementById('new-dimensions').textContent = `${width} x ${height}`;
                    
                    // Load the resized image preview
                    const resizedImgPreview = document.getElementById('resized-image-preview');
                    
                    // Add timestamp to bypass cache
                    resizedImgPreview.src = data.download_url + '?t=' + new Date().getTime();
                    
                    // Show result container
                    window.showResultContainer();
                } else {
                    // Show error message
                    window.showErrorContainer(data.error || "An error occurred while resizing the image.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
});
