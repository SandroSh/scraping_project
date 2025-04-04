from typing import Dict, Optional
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context
from error_handler import handle_http_error
from time import time, sleep
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

class SSLAdapter(HTTPAdapter):
    """
        Adapter for secure SSL configuration
    """
    
    def __init__(self, ssl_version = ssl.PROTOCOL_TLSv1_2):
        self.ssl_version = ssl_version
        super().__init__()
        
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ssl_version=self.ssl_version)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        kwargs['ssl_context'] = context
        return PoolManager(*args, **kwargs)


def get_request(url: str, auth_token: Optional[str] = None, custom_headers: Optional[Dict] = None, timeout: int = 10) -> str:
    """
    Fetch web content from a given URL using a GET request with headers, with rate limiting.
    Args:
        url (str)
        auth_token (str, optional)
        custom_headers (dict, optional)
        timeout (int): maximum amount of waiting time 
    Returns:
        str: The raw content 
    Raises:
        requests.RequestException
    """
    # Static state to track request timestamps (persistent across calls)
    if not hasattr(get_request, 'request_times'):
        get_request.request_times = [] 
    if not hasattr(get_request, 'max_requests'):
        get_request.max_requests = 10  # Max requests per period
    if not hasattr(get_request, 'period'):
        get_request.period = 60  

    try:
        # Rate limiting logic
        current_time = time()
        
        # Remove timestamps older than the period
        get_request.request_times = [t for t in get_request.request_times if current_time - t < get_request.period]

        # Check if we've hit the limit
        if len(get_request.request_times) >= get_request.max_requests:
            
            # Wait until the oldest request falls out of the period
            sleep_time = get_request.period - (current_time - get_request.request_times[0])
            sleep(sleep_time)
          
            current_time = time()
            get_request.request_times = [t for t in get_request.request_times if current_time - t < get_request.period]

       
        get_request.request_times.append(current_time)

   
        session = requests.Session()
        session.mount('https://', SSLAdapter())
        
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
      
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
      
        if custom_headers:
            headers.update(custom_headers)
        
        response = session.get(url, headers=headers, timeout=timeout, verify=True)
        response.raise_for_status()
        return response.text
    
    except requests.RequestException as e:
        error_message = handle_http_error(e)
        raise requests.RequestException(error_message)
    finally:
        session.close()

