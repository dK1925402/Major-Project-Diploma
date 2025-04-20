// qrcode.js - Handles QR code generation functionality

document.addEventListener('DOMContentLoaded', function() {
    // QR Code Generator Form
    const qrGeneratorForm = document.getElementById('qr-generator-form');
    if (qrGeneratorForm) {
        const dataType = document.getElementById('data-type');
        const dataInputs = document.querySelectorAll('.data-input');
        const generateBtn = document.getElementById('generate-btn');
        const togglePasswordBtn = document.getElementById('toggle-password');
        
        // Show/hide the appropriate input fields based on the selected data type
        dataType.addEventListener('change', function() {
            dataInputs.forEach(input => {
                input.style.display = 'none';
            });
            
            const selectedInput = document.getElementById(`${this.value}-input`);
            if (selectedInput) {
                selectedInput.style.display = 'block';
            }
        });
        
        // Toggle password visibility for WiFi password
        if (togglePasswordBtn) {
            togglePasswordBtn.addEventListener('click', function() {
                const passwordField = document.getElementById('wifi-password');
                const icon = this.querySelector('i');
                
                if (passwordField.type === 'password') {
                    passwordField.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    passwordField.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            });
        }
        
        // WiFi encryption selection logic
        const wifiEncryption = document.getElementById('wifi-encryption');
        const wifiPasswordContainer = document.getElementById('wifi-password-container');
        
        if (wifiEncryption && wifiPasswordContainer) {
            wifiEncryption.addEventListener('change', function() {
                if (this.value === 'nopass') {
                    wifiPasswordContainer.style.display = 'none';
                } else {
                    wifiPasswordContainer.style.display = 'block';
                }
            });
        }
        
        // Form submit handler
        qrGeneratorForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get the selected data type
            const selectedType = dataType.value;
            
            // Validation and data collection based on data type
            let qrData = '';
            let formValid = true;
            
            // URL
            if (selectedType === 'url') {
                const urlData = document.getElementById('url-data').value;
                if (!urlData) {
                    formValid = false;
                    alert('Please enter a valid URL');
                } else {
                    qrData = urlData;
                }
            }
            // Text
            else if (selectedType === 'text') {
                const textData = document.getElementById('text-data').value;
                if (!textData) {
                    formValid = false;
                    alert('Please enter some text');
                } else {
                    qrData = textData;
                }
            }
            // Email
            else if (selectedType === 'email') {
                const emailData = document.getElementById('email-data').value;
                const emailSubject = document.getElementById('email-subject').value;
                const emailBody = document.getElementById('email-body').value;
                
                if (!emailData) {
                    formValid = false;
                    alert('Please enter a valid email address');
                } else {
                    qrData = `mailto:${emailData}`;
                    
                    if (emailSubject || emailBody) {
                        qrData += '?';
                        if (emailSubject) {
                            qrData += `subject=${encodeURIComponent(emailSubject)}`;
                        }
                        if (emailSubject && emailBody) {
                            qrData += '&';
                        }
                        if (emailBody) {
                            qrData += `body=${encodeURIComponent(emailBody)}`;
                        }
                    }
                }
            }
            // Phone
            else if (selectedType === 'phone') {
                const phoneData = document.getElementById('phone-data').value;
                if (!phoneData) {
                    formValid = false;
                    alert('Please enter a valid phone number');
                } else {
                    qrData = `tel:${phoneData}`;
                }
            }
            // SMS
            else if (selectedType === 'sms') {
                const smsNumber = document.getElementById('sms-number').value;
                const smsMessage = document.getElementById('sms-message').value;
                
                if (!smsNumber) {
                    formValid = false;
                    alert('Please enter a valid phone number');
                } else {
                    qrData = `smsto:${smsNumber}`;
                    if (smsMessage) {
                        qrData += `:${smsMessage}`;
                    }
                }
            }
            // WiFi
            else if (selectedType === 'wifi') {
                const wifiSsid = document.getElementById('wifi-ssid').value;
                const wifiEncryption = document.getElementById('wifi-encryption').value;
                const wifiPassword = document.getElementById('wifi-password').value;
                const wifiHidden = document.getElementById('wifi-hidden').checked;
                
                if (!wifiSsid) {
                    formValid = false;
                    alert('Please enter a network name (SSID)');
                } else if (wifiEncryption !== 'nopass' && !wifiPassword) {
                    formValid = false;
                    alert('Please enter a WiFi password');
                } else {
                    qrData = `WIFI:S:${wifiSsid};T:${wifiEncryption};`;
                    if (wifiEncryption !== 'nopass') {
                        qrData += `P:${wifiPassword};`;
                    }
                    if (wifiHidden) {
                        qrData += 'H:true;';
                    }
                    qrData += ';';
                }
            }
            // vCard
            else if (selectedType === 'vcard') {
                const firstName = document.getElementById('vcard-firstname').value;
                const lastName = document.getElementById('vcard-lastname').value;
                const company = document.getElementById('vcard-company').value;
                const title = document.getElementById('vcard-title').value;
                const phone = document.getElementById('vcard-phone').value;
                const email = document.getElementById('vcard-email').value;
                const website = document.getElementById('vcard-website').value;
                const address = document.getElementById('vcard-address').value;
                const city = document.getElementById('vcard-city').value;
                const state = document.getElementById('vcard-state').value;
                const zipcode = document.getElementById('vcard-zipcode').value;
                const country = document.getElementById('vcard-country').value;
                
                if (!firstName || !phone || !email) {
                    formValid = false;
                    alert('Please fill in all required fields (First Name, Phone, and Email)');
                } else {
                    qrData = 'BEGIN:VCARD\nVERSION:3.0\n';
                    qrData += `N:${lastName};${firstName};;;\n`;
                    qrData += `FN:${firstName} ${lastName}\n`;
                    
                    if (company) {
                        qrData += `ORG:${company}\n`;
                    }
                    
                    if (title) {
                        qrData += `TITLE:${title}\n`;
                    }
                    
                    qrData += `TEL:${phone}\n`;
                    qrData += `EMAIL:${email}\n`;
                    
                    if (website) {
                        qrData += `URL:${website}\n`;
                    }
                    
                    // Build address if provided
                    let adrParts = [];
                    if (address || city || state || zipcode || country) {
                        qrData += 'ADR:;;';
                        if (address) adrParts.push(address);
                        if (city) adrParts.push(city);
                        if (state) adrParts.push(state);
                        if (zipcode) adrParts.push(zipcode);
                        if (country) adrParts.push(country);
                        
                        qrData += adrParts.join(';');
                        qrData += '\n';
                    }
                    
                    qrData += 'END:VCARD';
                }
            }
            
            if (!formValid) {
                return;
            }
            
            // Show progress container
            window.showProgressContainer();
            
            // Create form data
            const formData = new FormData();
            formData.append('data', qrData);
            
            // Make AJAX request to the server
            fetch('/api/generate-qr', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Set download link
                    const downloadLink = document.getElementById('download-link');
                    downloadLink.href = data.download_url;
                    
                    // Load the QR code preview
                    const qrCodePreview = document.getElementById('qr-code-preview');
                    
                    // Add timestamp to bypass cache
                    qrCodePreview.src = data.download_url + '?t=' + new Date().getTime();
                    
                    // Show result container
                    window.showResultContainer();
                } else {
                    // Show error message
                    window.showErrorContainer(data.error || "An error occurred while generating the QR code.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                window.showErrorContainer("An unexpected error occurred. Please try again.");
            });
        });
    }
});
