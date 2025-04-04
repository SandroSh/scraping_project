from typing import Dict, Optional
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context


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
    