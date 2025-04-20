import os
import logging
from pytube import YouTube
import subprocess

logger = logging.getLogger(__name__)

def download_youtube_video(video_url, output_path, quality='720p'):
    """
    Download a YouTube video with the specified quality.
    
    Args:
        video_url (str): The URL of the YouTube video
        output_path (str): The path to save the downloaded video
        quality (str): The quality of the video (e.g., '360p', '720p', '1080p')
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Downloading YouTube video: {video_url} at {quality} quality")
        
        # Create a YouTube object
        yt = YouTube(video_url)
        
        # Get the appropriate stream based on the quality
        if quality == '360p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()
        elif quality == '480p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res='480p').first()
        elif quality == '720p':
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res='720p').first()
        elif quality == '1080p':
            # 1080p often requires separate audio and video streams
            stream = yt.streams.filter(adaptive=True, file_extension='mp4', res='1080p').first()
            if not stream:
                # Fallback to highest resolution available
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            # Default to highest quality available
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            # If no stream found with the exact quality, get the highest available
            logger.warning(f"No {quality} quality stream found, getting highest available.")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            return {'success': False, 'error': f"No suitable stream found for {video_url}"}
        
        # Download the video
        stream.download(filename=output_path)
        
        return {'success': True}
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {str(e)}")
        return {'success': False, 'error': str(e)}

def convert_youtube_to_mp3(video_url, output_path):
    """
    Download a YouTube video and convert it to MP3.
    
    Args:
        video_url (str): The URL of the YouTube video
        output_path (str): The path to save the MP3 file
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Converting YouTube video to MP3: {video_url}")
        
        # Create a YouTube object
        yt = YouTube(video_url)
        
        # Get the audio stream with highest quality
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not stream:
            return {'success': False, 'error': f"No audio stream found for {video_url}"}
        
        # Download the audio to a temporary file
        temp_file = f"{output_path}.temp"
        stream.download(filename=temp_file)
        
        # Use ffmpeg to convert to MP3
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
        
        # Check if conversion was successful
        if process.returncode != 0:
            logger.error(f"ffmpeg error: {stderr.decode()}")
            return {'success': False, 'error': f"Error converting to MP3: {stderr.decode()}"}
        
        # Remove temporary file
        os.remove(temp_file)
        
        return {'success': True}
    except Exception as e:
        logger.error(f"Error converting YouTube to MP3: {str(e)}")
        return {'success': False, 'error': str(e)}
