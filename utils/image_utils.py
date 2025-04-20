import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)

def resize_image(input_path, output_path, width, height):
    """
    Resize an image to the specified dimensions.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path to save the resized image
        width (int): Desired width in pixels
        height (int): Desired height in pixels
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Resizing image to {width}x{height}: {input_path}")
        
        # Open the image
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize((width, height), Image.LANCZOS)
            
            # Save the resized image
            resized_img.save(output_path, quality=95)
        
        # Verify the output file exists and has non-zero size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True}
        else:
            return {'success': False, 'error': "Failed to create resized image"}
    
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return {'success': False, 'error': str(e)}
