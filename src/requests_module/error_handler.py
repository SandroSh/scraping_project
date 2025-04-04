from typing import Optional
import requests

def handle_http_error(error: requests.RequestException) -> str:
    
    if not isinstance(error, requests.RequestException):
        return "Different error type provided insted of Request error type"
    
    if not hasattr(error, 'response') or error.response is None:
        if isinstance(error, requests.ConnectionError):
            return "Connection Error: Failed to connect to the server"
        elif isinstance(error, requests.Timeout):
            return "Timeout Error: the request timed out"
        elif isinstance(error, requests.TooManyRedirects):
            return "Redirect error: too many redirections"
        return f"Network Error {str(error)}"
    
    STATUS_CODE = error.response.status_code

    error_messages = {
        400: "Bad Request (400): The server couldn't understand the request",
        401: "Unauthorized (401): Authentication required",
        403: "Forbidden (403): Access denied",
        404: "Not Found (404): Resource not found",
        408: "Request Timeout (408): Server timed out waiting for request",
        429: "Too Many Requests (429): Rate limit exceeded",
        500: "Server Error (500): Internal server error",
        502: "Bad Gateway (502): Invalid response from upstream server",
        503: "Service Unavailable (503): Server temporarily down",
        504: "Gateway Timeout (504): Upstream server failed to respond"
    }
    
    return error_messages.get(STATUS_CODE, f"HTTP error ({STATUS_CODE}) : {str(error)}")