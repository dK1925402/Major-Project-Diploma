import os
import logging
from PyPDF2 import PdfMerger
from PIL import Image

logger = logging.getLogger(__name__)

def merge_pdfs(pdf_paths, output_path):
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        pdf_paths (list): List of paths to the PDF files
        output_path (str): Path to save the merged PDF
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Merging {len(pdf_paths)} PDF files")
        
        # Create a PDF merger object
        merger = PdfMerger()
        
        # Add each PDF to the merger
        for pdf_path in pdf_paths:
            merger.append(pdf_path)
        
        # Write the merged PDF to the output path
        merger.write(output_path)
        merger.close()
        
        # Verify the output file exists and has non-zero size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True}
        else:
            return {'success': False, 'error': "Failed to create merged PDF file"}
    
    except Exception as e:
        logger.error(f"Error merging PDFs: {str(e)}")
        return {'success': False, 'error': str(e)}

def images_to_pdf(image_paths, output_path):
    """
    Convert multiple images to a single PDF file.
    
    Args:
        image_paths (list): List of paths to the image files
        output_path (str): Path to save the PDF file
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Converting {len(image_paths)} images to PDF")
        
        # Check if there are any images to convert
        if not image_paths:
            return {'success': False, 'error': "No images provided for conversion"}
        
        # Open the first image to get the size
        images = []
        for path in image_paths:
            img = Image.open(path)
            
            # Convert to RGB if image is in another mode (like RGBA)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            images.append(img)
        
        # Save the images as a PDF
        first_image = images[0]
        if len(images) == 1:
            first_image.save(output_path, "PDF", resolution=100.0)
        else:
            first_image.save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        
        # Verify the output file exists and has non-zero size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True}
        else:
            return {'success': False, 'error': "Failed to create PDF from images"}
    
    except Exception as e:
        logger.error(f"Error converting images to PDF: {str(e)}")
        return {'success': False, 'error': str(e)}
