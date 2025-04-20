import os
import uuid
import time
import logging
import subprocess
import yt_dlp

logger = logging.getLogger(__name__)

def download_instagram_reel(post_url, output_path):
    """
    Download an Instagram reel using yt-dlp.
    
    Args:
        post_url (str): The URL of the Instagram post/reel
        output_path (str): The path to save the downloaded video
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Downloading Instagram reel: {post_url}")
        
        # Clean the URL (remove query parameters if present)
        if '?' in post_url:
            post_url = post_url.split('?')[0]
        
        # Add trailing slash if not present
        if not post_url.endswith('/'):
            post_url += '/'
            
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'prefer_ffmpeg': True,
            'retries': 5,
            'fragment_retries': 5,
            'cookiefile': None,  # You can add cookies for authentication if needed
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(post_url, download=True)
            if info_dict is None:
                # If yt-dlp failed, try another method with pure ffmpeg
                return download_instagram_reel_fallback(post_url, output_path)
                
            # Get the title or description if available
            title = info_dict.get('title', 'Instagram Reel')
            description = info_dict.get('description', '')
            
        # Verify download was successful
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True, 'title': title, 'description': description}
        else:
            # Try fallback method
            return download_instagram_reel_fallback(post_url, output_path)
    
    except Exception as e:
        logger.error(f"Error downloading Instagram reel with yt-dlp: {str(e)}")
        # Try fallback method
        return download_instagram_reel_fallback(post_url, output_path)


def download_instagram_reel_fallback(post_url, output_path):
    """
    Fallback method to download Instagram reel using direct ffmpeg.
    
    Args:
        post_url (str): The URL of the Instagram post/reel
        output_path (str): The path to save the downloaded video
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Using fallback method to download Instagram reel: {post_url}")
        
        # Use ffmpeg with instagram URL directly (ffmpeg can sometimes extract the video directly)
        cmd = [
            'ffmpeg',
            '-headers', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            '-i', post_url,
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            '-movflags', 'faststart',
            output_path
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Check if download was successful
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True, 'title': 'Instagram Reel', 'description': ''}
        else:
            logger.error(f"Fallback failed: {stderr.decode()}")
            return {'success': False, 'error': "All download methods failed. Please try a different Instagram reel URL."}
    
    except Exception as e:
        logger.error(f"Error in Instagram reel fallback: {str(e)}")
        return {'success': False, 'error': str(e)}
