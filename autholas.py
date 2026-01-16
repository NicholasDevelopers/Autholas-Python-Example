# pip install requests
import requests
import hashlib
import platform
import getpass

# Your API configuration
API_KEY = "YOUR_API_KEY_HERE"
API_URL = "https://autholas.web.id/api/auth"

def get_hardware_id():
    """Generate hardware ID"""
    hostname = platform.node()
    username = getpass.getuser()
    architecture = platform.machine().lower()

    # Normalize architecture like Node.js
    if architecture == "amd64":
        architecture = "x64"
    elif architecture == "x86_64":
        architecture = "x64"

    combined = f"{hostname}|{username}|{architecture}"
    return hashlib.sha256(combined.encode()).hexdigest()

def handle_auth_error(error_code, error_message):
    error_messages = {
        'INVALID_CREDENTIALS': {
            'title': 'Login Failed',
            'message': 'Username or password is incorrect.\nPlease double-check your credentials and try again.'
        },
        'USER_BANNED': {
            'title': 'Account Banned',
            'message': 'Your account has been suspended.\nPlease contact support for assistance.'
        },
        'SUBSCRIPTION_EXPIRED': {
            'title': 'Subscription Expired',
            'message': 'Your subscription has ended.\nPlease renew your subscription to continue.'
        },
        'MAX_DEVICES_REACHED': {
            'title': 'Device Limit Reached',
            'message': 'Maximum number of devices exceeded.\nPlease contact support to reset your devices.'
        },
        'HWID_BANNED': {
            'title': 'Device Banned',
            'message': 'This device has been banned.\nPlease contact support for assistance.'
        },
        'INVALID_API_KEY': {
            'title': 'Service Error',
            'message': 'Authentication service unavailable.\nPlease try again later or contact support.'
        },
        'RATE_LIMIT_EXCEEDED': {
            'title': 'Too Many Attempts',
            'message': 'Please wait before trying again.'
        },
        'DEVELOPER_SUSPENDED': {
            'title': 'Service Unavailable',
            'message': 'Authentication service is temporarily unavailable.\nPlease contact support.'
        },
        'SERVICE_ERROR': {
            'title': 'Service Error',
            'message': 'Authentication service is temporarily unavailable.\nPlease try again later.'
        }
    }
    
    if error_code in error_messages:
        error = error_messages[error_code]
        print(error['title'])
        print(error['message'])
    else:
        print(f"Error: {error_message}")

def authenticate(username, password, hwid):
    payload = {
        'api_key': API_KEY,
        'username': username,
        'password': password,
        'hwid': hwid,
        'device_name': 'User PC'
    }
    
    try:
        print("Authenticating...")
        response = requests.post(API_URL, json=payload, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print("Login successful!")
            print(f"Welcome, {username}!")
            print(f"Session token: {result.get('session_token')}")
            print(f"Session expires: {result.get('expires_at')}")
            print(f"Subscription expires: {result['user']['expires_at']}")

            return {'success': True, 'session_token': result.get('session_token')}
        else:
            error_code = result.get('error_code', 'UNKNOWN')
            error_message = result.get('error', 'Unknown error')
            handle_auth_error(error_code, error_message)
            return {'success': False, 'error': error_message, 'error_code': error_code}
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")

        return {'success': False, 'error': str(e)}

