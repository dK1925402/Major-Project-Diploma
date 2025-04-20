import os
import uuid
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app

# Import utility modules
from utils.youtube_utils import download_youtube_video, convert_youtube_to_mp3
from utils.instagram_utils import download_instagram_reel
from utils.document_utils import merge_pdfs, images_to_pdf
from utils.image_utils import resize_image
from utils.qrcode_utils import generate_qr_code

# Main index route
@app.route('/')
def index():
    return render_template('index.html')

# YouTube Video Downloader
@app.route('/youtube-downloader')
def youtube_downloader():
    return render_template('youtube_downloader.html')

@app.route('/api/youtube-download', methods=['POST'])
def api_youtube_download():
    try:
        video_url = request.form.get('video_url')
        quality = request.form.get('quality', '720p')
        
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Download the video
        result = download_youtube_video(video_url, output_path, quality)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Video downloaded successfully',
                'title': result.get('title', 'YouTube Video'),
                'download_url': url_for('download_file', filename=filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in YouTube download: {str(e)}")
        return jsonify({'error': str(e)}), 500

# YouTube to MP3 Converter
@app.route('/youtube-to-mp3')
def youtube_to_mp3():
    return render_template('youtube_to_mp3.html')

@app.route('/api/youtube-to-mp3', methods=['POST'])
def api_youtube_to_mp3():
    try:
        video_url = request.form.get('video_url')
        
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp3"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Convert YouTube video to MP3
        result = convert_youtube_to_mp3(video_url, output_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Audio extracted successfully',
                'title': result.get('title', 'YouTube Audio'),
                'download_url': url_for('download_file', filename=filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in YouTube to MP3 conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Instagram Reel Downloader
@app.route('/instagram-downloader')
def instagram_downloader():
    return render_template('instagram_downloader.html')

@app.route('/api/instagram-download', methods=['POST'])
def api_instagram_download():
    try:
        post_url = request.form.get('post_url')
        
        if not post_url:
            return jsonify({'error': 'Instagram post URL is required'}), 400

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Download Instagram reel
        result = download_instagram_reel(post_url, output_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Instagram reel downloaded successfully',
                'title': result.get('title', 'Instagram Reel'),
                'description': result.get('description', ''),
                'download_url': url_for('download_file', filename=filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in Instagram download: {str(e)}")
        return jsonify({'error': str(e)}), 500

# PDF Merger
@app.route('/pdf-merger')
def pdf_merger():
    return render_template('pdf_merger.html')

@app.route('/api/merge-pdfs', methods=['POST'])
def api_merge_pdfs():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No PDF files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No PDF files selected'}), 400
    
    try:
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_PDF_EXTENSIONS']:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                temp_files.append(file_path)
            else:
                return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
        
        if len(temp_files) < 2:
            return jsonify({'error': 'At least two PDF files are required for merging'}), 400
        
        # Generate output filename
        output_filename = f"merged_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Merge PDFs
        result = merge_pdfs(temp_files, output_path)
        
        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'PDF files merged successfully',
                'download_url': url_for('download_file', filename=output_filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in PDF merger: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Image to PDF
@app.route('/image-to-pdf')
def image_to_pdf():
    return render_template('image_to_pdf.html')

@app.route('/api/images-to-pdf', methods=['POST'])
def api_images_to_pdf():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No image files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No image files selected'}), 400
    
    try:
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                temp_files.append(file_path)
            else:
                return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
        
        # Generate output filename
        output_filename = f"document_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Convert images to PDF
        result = images_to_pdf(temp_files, output_path)
        
        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Images converted to PDF successfully',
                'download_url': url_for('download_file', filename=output_filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in images to PDF conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Image Resizer
@app.route('/image-resizer')
def image_resizer():
    return render_template('image_resizer.html')

@app.route('/api/resize-image', methods=['POST'])
def api_resize_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400
    
    if not file or '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400
    
    try:
        width = request.form.get('width')
        height = request.form.get('height')
        
        # Validate dimensions
        if not width or not height:
            return jsonify({'error': 'Width and height are required'}), 400
        
        try:
            width = int(width)
            height = int(height)
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers")
        except ValueError:
            return jsonify({'error': 'Width and height must be positive integers'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Generate output filename with same extension
        ext = filename.rsplit('.', 1)[1].lower()
        output_filename = f"resized_{uuid.uuid4()}.{ext}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Resize image
        result = resize_image(input_path, output_path, width, height)
        
        # Clean up input file
        if os.path.exists(input_path):
            os.remove(input_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Image resized successfully',
                'download_url': url_for('download_file', filename=output_filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in image resizing: {str(e)}")
        return jsonify({'error': str(e)}), 500

# QR Code Generator
@app.route('/qr-generator')
def qr_generator():
    return render_template('qr_generator.html')

@app.route('/api/generate-qr', methods=['POST'])
def api_generate_qr():
    try:
        data = request.form.get('data')
        
        if not data:
            return jsonify({'error': 'QR code data is required'}), 400
        
        # Generate output filename
        output_filename = f"qrcode_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Generate QR code
        result = generate_qr_code(data, output_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'QR code generated successfully',
                'download_url': url_for('download_file', filename=output_filename)
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        app.logger.error(f"Error in QR code generation: {str(e)}")
        return jsonify({'error': str(e)}), 500

# File download handler
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error in file download: {str(e)}")
        flash('Error downloading file', 'danger')
        return redirect(url_for('index'))
