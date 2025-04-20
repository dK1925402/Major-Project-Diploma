import os
import uuid
import time
import json
import logging
import requests
import subprocess
import re

logger = logging.getLogger(__name__)

def download_instagram_reel(post_url, output_path):
    """
    Download an Instagram reel or post video.
    Uses a combination of methods to ensure successful downloads.
    
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
        
        # Method 1: Try direct method using API endpoints
        result = download_via_api(post_url, output_path)
        if result['success']:
            return result
            
        # Method 2: Try extraction from page source
        result = download_via_page_source(post_url, output_path)
        if result['success']:
            return result
            
        # Method 3: Try with the Instagram downloader service
        result = download_via_service(post_url, output_path)
        if result['success']:
            return result
        
        # All methods failed
        return {'success': False, 'error': "Could not download Instagram media. Please ensure the URL is correct and the content is public."}
    
    except Exception as e:
        logger.error(f"Error downloading Instagram media: {str(e)}")
        return {'success': False, 'error': f"Error: {str(e)}"}


def download_via_api(post_url, output_path):
    """
    Attempt to download using Instagram's API endpoints
    """
    try:
        # Extract the shortcode from the URL
        shortcode = post_url.split('/')[-2]
        if not shortcode:
            return {'success': False, 'error': "Could not extract post ID from URL"}
        
        # Request headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Try to fetch the page to extract media data
        response = requests.get(post_url, headers=headers)
        if response.status_code != 200:
            return {'success': False, 'error': f"Failed to access Instagram page (status code: {response.status_code})"}
        
        # Try to extract the video URL from the page source
        html_content = response.text
        
        # First attempt: Look for video URL in og:video meta tag
        og_video_match = re.search(r'<meta property="og:video" content="([^"]+)"', html_content)
        if og_video_match:
            video_url = og_video_match.group(1)
            return download_from_url(video_url, output_path, headers)
        
        # Second attempt: Look for video URL in shared_data JSON
        shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});</script>', html_content, re.DOTALL)
        if shared_data_match:
            try:
                shared_data = json.loads(shared_data_match.group(1))
                media = None
                
                # Navigate through the JSON structure to find video URL
                if 'entry_data' in shared_data and 'PostPage' in shared_data['entry_data']:
                    post = shared_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                    if post['is_video']:
                        video_url = post['video_url']
                        return download_from_url(video_url, output_path, headers)
            except Exception as e:
                logger.error(f"Error extracting from shared data: {str(e)}")
        
        # Third attempt: Look for additional_data JSON
        additional_data_match = re.search(r'window\.__additionalDataLoaded\s*\(\s*[\'"][^\'"]+[\'"],\s*({.*?})\s*\)', html_content, re.DOTALL)
        if additional_data_match:
            try:
                additional_data = json.loads(additional_data_match.group(1))
                if 'graphql' in additional_data and 'shortcode_media' in additional_data['graphql']:
                    post = additional_data['graphql']['shortcode_media']
                    if post['is_video']:
                        video_url = post['video_url']
                        return download_from_url(video_url, output_path, headers)
            except Exception as e:
                logger.error(f"Error extracting from additional data: {str(e)}")
        
        return {'success': False, 'error': "Could not find video URL in the page source"}
    
    except Exception as e:
        logger.error(f"Error in API download method: {str(e)}")
        return {'success': False, 'error': str(e)}


def download_via_page_source(post_url, output_path):
    """
    Attempt to extract video URL from the page source using regex patterns
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        response = requests.get(post_url, headers=headers)
        if response.status_code != 200:
            return {'success': False, 'error': "Failed to access Instagram page"}
        
        html_content = response.text
        
        # Pattern for finding video URLs in the page
        video_url_patterns = [
            r'"video_url":"([^"]+)"',
            r'"video_url":"([^"]+)"',
            r'<meta property="og:video" content="([^"]+)"',
            r'<meta property="og:video:secure_url" content="([^"]+)"',
            r'"contentUrl":"([^"]+\.mp4[^"]*)"'
        ]
        
        for pattern in video_url_patterns:
            match = re.search(pattern, html_content)
            if match:
                video_url = match.group(1).replace('\\u0026', '&')
                return download_from_url(video_url, output_path, headers)
        
        # Extract title and description if possible
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html_content)
        title = title_match.group(1) if title_match else "Instagram Post"
        
        desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content)
        description = desc_match.group(1) if desc_match else ""
        
        return {'success': False, 'error': "Could not find video URL in page source", 'title': title, 'description': description}
    
    except Exception as e:
        logger.error(f"Error in page source download method: {str(e)}")
        return {'success': False, 'error': str(e)}


def download_via_service(post_url, output_path):
    """
    Attempt to download using a third-party service if direct methods fail
    """
    try:
        # This is a placeholder - in a real implementation, you might use a reliable
        # third-party service API to download Instagram content when direct methods fail
        # For demonstration purposes, we'll return a failure
        return {'success': False, 'error': "Third-party download services not implemented"}
    
    except Exception as e:
        logger.error(f"Error in service download method: {str(e)}")
        return {'success': False, 'error': str(e)}


def download_from_url(video_url, output_path, headers=None):
    """
    Download video from direct URL to the specified output path
    """
    try:
        if not headers:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        
        # Stream the download to handle large files
        with requests.get(video_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Verify file was downloaded successfully
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {
                'success': True, 
                'title': 'Instagram Video', 
                'description': 'Downloaded from Instagram'
            }
        else:
            return {'success': False, 'error': "Download failed - empty file created"}
    
    except Exception as e:
        logger.error(f"Error downloading from URL: {str(e)}")
        return {'success': False, 'error': f"Download error: {str(e)}"}
