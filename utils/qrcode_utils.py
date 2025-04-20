import os
import logging
import qrcode

logger = logging.getLogger(__name__)

def generate_qr_code(data, output_path):
    """
    Generate a QR code from the given data and save it to the specified path.
    
    Args:
        data (str): The data to encode in the QR code
        output_path (str): Path to save the QR code image
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Generating QR code for data: {data[:30]}...")
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(output_path)
        
        # Verify the output file exists and has non-zero size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True}
        else:
            return {'success': False, 'error': "Failed to create QR code image"}
    
    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        return {'success': False, 'error': str(e)}
