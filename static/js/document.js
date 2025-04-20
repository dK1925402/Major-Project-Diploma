// document.js - Handles PDF merger and Image to PDF conversion functionality

document.addEventListener('DOMContentLoaded', function() {
    // Common variables
    let selectedFiles = [];
    
    // PDF Merger Form
    const pdfMergerForm = document.getElementById('pdf-merger-form');
    if (pdfMergerForm) {
        const pdfInput = document.getElementById('pdf-files');
        const selectedFilesContainer = document.getElementById('selected-files-container');
        const selectedFilesList = document.getElementById('selected-files-list');
        const clearFilesBtn = document.getElementById('clear-files-btn');
        const mergeBtn = document.getElementById('merge-btn');
        
        // File selection change handler
        pdfInput.addEventListener('change', function(event) {
            const files = Array.from(event.target.files);
            
            if (files.length === 0) {
                selectedFilesContainer.style.display = 'none';
                mergeBtn.disabled = true;
                return;
            }
            
            // Store selected files
            selectedFiles = files;
            
            // Display selected files
            selectedFilesContainer.style.display = 'block';
            selectedFilesList.innerHTML = '';
            
            files.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'selected-file-item';
                fileItem.innerHTML = `
                    <div class="file-info">
                        <span class="file-name">${file.name}</span>
                        <small class="file-size">${window.humanFileSize(file.size)}</small>
                    </div>
                    <button type="button" class="remove-file-btn" data-index="${index}">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                selectedFilesList.appendChild(fileItem);
            });
            
            // Enable merge button if at least two files are selected
            mergeBtn.disabled = files.length < 2;
            
            // Add click event for remove buttons
            const removeButtons = document.querySelectorAll('.remove-file-btn');
            removeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    removeFile(index);
                });
            });
        });
        
        // Clear all files
        clearFilesBtn.addEventListener('click', function() {
            selectedFiles = [];
            selectedFilesContainer.style.display = 'none';
            selectedFilesList.innerHTML = '';
            pdfInput.value = '';
            mergeBtn.disabled = true;
        });
        
        // Function to remove a specific file
        function removeFile(index) {
            // Create a new FileList-like object without the removed file
            const dt = new DataTransfer();
            
            Array.from(pdfInput.files)
                .filter((file, idx) => idx !== index)
                .forEach(file => dt.items.add(file));
            
            // Update the input's files property
            pdfInput.files = dt.files;
            
            // Trigger change event to update the UI
            const event = new Event('change');
            pdfInput.dispatchEvent(event);
        }
        
        // Form submit handler
        pdfMergerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity() || selectedFiles.length < 2) {
                this.classList.add('was-validated');
                return;
            }
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files[]', file);
            });
            
            // Make AJAX request to the server
            fetch('/api/merge-pdfs', {
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
                    window.showErrorContainer(data.error || "An error occurred while merging PDF files.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
    
    // Image to PDF Form
    const imageToPdfForm = document.getElementById('image-to-pdf-form');
    if (imageToPdfForm) {
        const imageInput = document.getElementById('image-files');
        const selectedFilesContainer = document.getElementById('selected-files-container');
        const selectedFilesList = document.getElementById('selected-files-list');
        const clearFilesBtn = document.getElementById('clear-files-btn');
        const convertBtn = document.getElementById('convert-btn');
        
        // File selection change handler
        imageInput.addEventListener('change', function(event) {
            const files = Array.from(event.target.files);
            
            if (files.length === 0) {
                selectedFilesContainer.style.display = 'none';
                convertBtn.disabled = true;
                return;
            }
            
            // Store selected files
            selectedFiles = files;
            
            // Display selected files
            selectedFilesContainer.style.display = 'block';
            selectedFilesList.innerHTML = '';
            
            files.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'selected-file-item';
                fileItem.innerHTML = `
                    <div class="file-info">
                        <span class="file-name">${file.name}</span>
                        <small class="file-size">${window.humanFileSize(file.size)}</small>
                    </div>
                    <button type="button" class="remove-file-btn" data-index="${index}">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                selectedFilesList.appendChild(fileItem);
            });
            
            // Enable convert button if at least one file is selected
            convertBtn.disabled = files.length < 1;
            
            // Add click event for remove buttons
            const removeButtons = document.querySelectorAll('.remove-file-btn');
            removeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    removeImage(index);
                });
            });
        });
        
        // Clear all files
        clearFilesBtn.addEventListener('click', function() {
            selectedFiles = [];
            selectedFilesContainer.style.display = 'none';
            selectedFilesList.innerHTML = '';
            imageInput.value = '';
            convertBtn.disabled = true;
        });
        
        // Function to remove a specific file
        function removeImage(index) {
            // Create a new FileList-like object without the removed file
            const dt = new DataTransfer();
            
            Array.from(imageInput.files)
                .filter((file, idx) => idx !== index)
                .forEach(file => dt.items.add(file));
            
            // Update the input's files property
            imageInput.files = dt.files;
            
            // Trigger change event to update the UI
            const event = new Event('change');
            imageInput.dispatchEvent(event);
        }
        
        // Form submit handler
        imageToPdfForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity() || selectedFiles.length < 1) {
                this.classList.add('was-validated');
                return;
            }
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files[]', file);
            });
            
            // Make AJAX request to the server
            fetch('/api/images-to-pdf', {
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
                    window.showErrorContainer(data.error || "An error occurred while converting images to PDF.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
});
