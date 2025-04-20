import os
import time
import uuid
import logging
import yt_dlp
import subprocess

logger = logging.getLogger(__name__)

def download_youtube_video(video_url, output_path, quality='720p'):
    """
    Download a YouTube video with the specified quality using yt-dlp.
    
    Args:
        video_url (str): The URL of the YouTube video
        output_path (str): The path to save the downloaded video
        quality (str): The quality of the video (e.g., '360p', '720p', '1080p')
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Downloading YouTube video: {video_url} at {quality} quality")
        
        # Map quality string to format
        quality_formats = {
            '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best[height<=360]',
            '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]',
            '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]',
            '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]'
        }
        
        # Get the format based on quality
        format_string = quality_formats.get(quality, 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]')
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': format_string,
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'prefer_ffmpeg': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            if info_dict is None:
                return {'success': False, 'error': 'Could not extract video information'}
            
            title = info_dict.get('title', 'YouTube Video')
        
        # Check if file exists and has size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True, 'title': title}
        else:
            return {'success': False, 'error': 'Download failed or empty file created'}
    
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {str(e)}")
        return {'success': False, 'error': str(e)}

def convert_youtube_to_mp3(video_url, output_path):
    """
    Download a YouTube video and convert it to MP3 using yt-dlp.
    
    Args:
        video_url (str): The URL of the YouTube video
        output_path (str): The path to save the MP3 file
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Converting YouTube video to MP3: {video_url}")
        
        # Directory where the file will be saved
        output_dir = os.path.dirname(output_path)
        output_filename = os.path.basename(output_path)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'writethumbnail': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        # Download and convert to MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            if info_dict is None:
                return {'success': False, 'error': 'Could not extract video information'}
            
            # Get the title and the final filename
            title = info_dict.get('title', 'YouTube Audio')
            
            # Find the downloaded MP3 file (should be in the output directory with .mp3 extension)
            downloaded_file = None
            for file in os.listdir(output_dir):
                if file.endswith(".mp3") and title in file:
                    downloaded_file = os.path.join(output_dir, file)
                    break
            
            # If we couldn't find the file this way, try other methods
            if not downloaded_file or not os.path.exists(downloaded_file):
                for file in os.listdir(output_dir):
                    if file.endswith(".mp3") and os.path.getmtime(os.path.join(output_dir, file)) > time.time() - 60:  # File created in the last minute
                        downloaded_file = os.path.join(output_dir, file)
                        break
            
            # Rename the downloaded file to the desired output path
            if downloaded_file and os.path.exists(downloaded_file):
                # If target file already exists, remove it
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(downloaded_file, output_path)
            else:
                # If we can't find the downloaded file, try a direct approach with ffmpeg
                temp_file = os.path.join(output_dir, f"temp_{uuid.uuid4()}.mp4")
                direct_dl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': temp_file,
                    'quiet': True,
                }
                
                with yt_dlp.YoutubeDL(direct_dl_opts) as direct_ydl:
                    direct_ydl.download([video_url])
                
                # Convert the temporary file to MP3 using ffmpeg
                cmd = [
                    'ffmpeg',
                    '-i', temp_file,
                    '-vn',  # No video
                    '-ar', '44100',  # Audio sample rate
                    '-ac', '2',  # Stereo
                    '-b:a', '192k',  # Bitrate
                    '-f', 'mp3',
                    output_path
                ]
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                # Remove temporary file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        # Check if file exists and has size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True, 'title': title}
        else:
            return {'success': False, 'error': 'Conversion failed or empty file created'}
    
    except Exception as e:
        logger.error(f"Error converting YouTube to MP3: {str(e)}")
        return {'success': False, 'error': str(e)}
