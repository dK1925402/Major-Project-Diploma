import os
import re
import json
import logging
import requests
import subprocess

logger = logging.getLogger(__name__)

def download_instagram_reel(post_url, output_path):
    """
    Download an Instagram reel using web requests.
    
    Args:
        post_url (str): The URL of the Instagram post/reel
        output_path (str): The path to save the downloaded video
    
    Returns:
        dict: A result dictionary containing success status and error message if any
    """
    try:
        logger.info(f"Downloading Instagram reel: {post_url}")
        
        # Clean the URL (remove query parameters)
        post_url = post_url.split('?')[0]
        
        # Add trailing slash if not present
        if not post_url.endswith('/'):
            post_url += '/'
        
        # Request the page with a user-agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(post_url, headers=headers)
        
        if response.status_code != 200:
            return {'success': False, 'error': f"Failed to fetch Instagram post: HTTP {response.status_code}"}
        
        # Try to find video URL in HTML content
        html_content = response.text
        
        # Instagram embeds video URLs in JSON data within script tags
        video_url = None
        
        # Method 1: Look for JSON data in script tags
        json_data_match = re.search(r'<script type="application/ld\+json">(.+?)</script>', html_content, re.DOTALL)
        if json_data_match:
            try:
                json_data = json.loads(json_data_match.group(1))
                if '@graph' in json_data:
                    for entry in json_data['@graph']:
                        if 'video' in entry and 'contentUrl' in entry['video']:
                            video_url = entry['video']['contentUrl']
                            break
            except Exception as e:
                logger.warning(f"Failed to parse Instagram JSON data: {str(e)}")
        
        # Method 2: Look for video URL directly
        if not video_url:
            video_match = re.search(r'<meta property="og:video" content="(.+?)"', html_content)
            if video_match:
                video_url = video_match.group(1)
        
        # Method 3: Look for video URL in another format
        if not video_url:
            video_match = re.search(r'video_url":"([^"]+)"', html_content)
            if video_match:
                video_url = video_match.group(1).replace('\\u0026', '&')
        
        if not video_url:
            return {'success': False, 'error': "Could not find video URL in Instagram post"}
        
        # Download the video
        video_response = requests.get(video_url, headers=headers, stream=True)
        
        if video_response.status_code != 200:
            return {'success': False, 'error': f"Failed to download video: HTTP {video_response.status_code}"}
        
        with open(output_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        # Verify download was successful
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {'success': True}
        else:
            return {'success': False, 'error': "Downloaded file is empty or does not exist"}
    
    except Exception as e:
        logger.error(f"Error downloading Instagram reel: {str(e)}")
        return {'success': False, 'error': str(e)}
