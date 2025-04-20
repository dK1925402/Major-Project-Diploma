// youtube.js - Handles YouTube downloader and YouTube to MP3 converter functionality

document.addEventListener('DOMContentLoaded', function() {
    // YouTube Video Downloader Form
    const youtubeForm = document.getElementById('youtube-form');
    if (youtubeForm) {
        youtubeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity()) {
                this.classList.add('was-validated');
                return;
            }
            
            const videoUrl = document.getElementById('video-url').value;
            const quality = document.getElementById('video-quality')?.value || '720p';
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            formData.append('video_url', videoUrl);
            formData.append('quality', quality);
            
            // Make AJAX request to the server
            fetch('/api/youtube-download', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Set download link
                    const downloadLink = document.getElementById('download-link');
                    downloadLink.href = data.download_url;
                    
                    // Set video title if available
                    if (data.title) {
                        document.getElementById('video-title').textContent = data.title;
                    } else {
                        document.getElementById('video-title').textContent = "Your YouTube video has been successfully downloaded.";
                    }
                    
                    // Show result container
                    window.showResultContainer();
                } else {
                    // Show error message
                    window.showErrorContainer(data.error || "An error occurred while downloading the video.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
    
    // YouTube to MP3 Converter Form
    const mp3Form = document.getElementById('mp3-form');
    if (mp3Form) {
        mp3Form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!this.checkValidity()) {
                this.classList.add('was-validated');
                return;
            }
            
            const videoUrl = document.getElementById('video-url').value;
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            formData.append('video_url', videoUrl);
            
            // Make AJAX request to the server
            fetch('/api/youtube-to-mp3', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Set download link
                    const downloadLink = document.getElementById('download-link');
                    downloadLink.href = data.download_url;
                    
                    // Set audio title if available
                    if (data.title) {
                        document.getElementById('audio-title').textContent = data.title;
                    } else {
                        document.getElementById('audio-title').textContent = "Your MP3 file has been successfully extracted.";
                    }
                    
                    // Show result container
                    window.showResultContainer();
                } else {
                    // Show error message
                    window.showErrorContainer(data.error || "An error occurred while converting the video to MP3.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
});
