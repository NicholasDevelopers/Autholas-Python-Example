# Autholas Python Authentication System

A Python implementation for Autholas authentication service with hardware ID verification.

## Features

- User authentication via Autholas API
- Hardware ID generation using system information
- Cross-platform support (Windows/Linux/macOS)
- Built-in SHA-256 hashing
- Comprehensive error handling
- Hidden password input

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Install Required Dependencies

```bash
pip install requests
```

**Alternative installation methods:**

```bash
# Using pip3 (if you have both Python 2 and 3)
pip3 install requests

# Using virtual environment (recommended)
python -m venv autholas_env
source autholas_env/bin/activate  # On Windows: autholas_env\Scripts\activate
pip install requests

# Using requirements.txt
echo "requests>=2.25.0" > requirements.txt
pip install -r requirements.txt
```

## File Structure

```
├── autholas.py         # Authentication functions and utilities
├── main.py             # Main program entry point
├── requirements.txt    # Dependencies (optional)
└── README.md          # This file
```

## Configuration

1. Open `autholas.py`
2. Replace `YOUR_API_KEY_HERE` with your actual Autholas API key:
   ```python
   API_KEY = "your_actual_api_key_here"
   ```

## Usage

### Basic Usage

```bash
python main.py
```

### Using the Module in Your Code

```python
from autholas import authenticate, get_hardware_id

# Get hardware ID
hwid = get_hardware_id()
print(f"Hardware ID: {hwid}")

# Authenticate user
result = authenticate("username", "password", hwid)

if result['success']:
    print("Authentication successful!")
    session_token = result['session_token']
    # Use session_token for your application
else:
    print(f"Authentication failed: {result['error']}")
```

## Functions

### `get_hardware_id()`
Generates a unique hardware ID based on:
- System hostname
- Username
- System architecture (normalized to match other implementations)

### `authenticate(username, password, hwid)`
Authenticates user with Autholas API and returns:
```python
{
    'success': True/False,
    'session_token': 'token_string',  # Only if success
    'error': 'error_message',         # Only if failed
    'error_code': 'ERROR_CODE'        # Only if failed
}
```

### `handle_auth_error(error_code, error_message)`
Displays user-friendly error messages for different error codes.

## Error Handling

The system handles various authentication errors:

- `INVALID_CREDENTIALS` - Wrong username/password
- `USER_BANNED` - Account suspended
- `SUBSCRIPTION_EXPIRED` - Subscription ended
- `MAX_DEVICES_REACHED` - Device limit exceeded
- `HWID_BANNED` - Device banned
- `RATE_LIMIT_EXCEEDED` - Too many attempts
- Network errors and timeouts

## Example Integration

```python
from autholas import authenticate, get_hardware_id
import getpass

def login_system():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hwid = get_hardware_id()
    
    result = authenticate(username, password, hwid)
    
    if result['success']:
        return result['session_token']
    else:
        print(f"Login failed: {result['error']}")
        return None

def main_application():
    session_token = login_system()
    if session_token:
        print("Welcome to the application!")
        # Your application logic here
    else:
        print("Access denied.")

if __name__ == "__main__":
    main_application()
```

## Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python -m venv autholas_env

# Activate virtual environment
# On Windows:
autholas_env\Scripts\activate
# On macOS/Linux:
source autholas_env/bin/activate

# Install dependencies
pip install requests

# Run the application
python main.py

# Deactivate when done
deactivate
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'requests'**
   ```bash
   pip install requests
   ```

2. **Permission denied (Windows)**
   ```bash
   # Run as administrator or use:
   pip install --user requests
   ```

3. **SSL Certificate errors**
   ```bash
   # Update certificates
   pip install --upgrade certifi
   ```

4. **Python not found**
   - Make sure Python is installed and added to PATH
   - Try using `python3` instead of `python`

### Testing Connection

```python
import requests

try:
    response = requests.get("https://httpbin.org/status/200", timeout=5)
    print("Internet connection OK")
except:
    print("Connection issues detected")
```

## Security Notes

- Never commit your API key to version control
- Use environment variables for production:
  ```python
  import os
  API_KEY = os.getenv('AUTHOLAS_API_KEY', 'YOUR_API_KEY_HERE')
  ```
- The hardware ID is generated locally and not stored

## Python Version Compatibility

- **Python 3.6+**: Full support
- **Python 2.7**: Not supported (use `requests` with caution)

For Python 2.7 compatibility (not recommended):
```bash
pip2 install requests
# Modify getpass import and f-strings in the code
```

## Dependencies

- **requests**: HTTP library for API communication
- **hashlib**: Built-in SHA-256 hashing (standard library)
- **platform**: System information (standard library)
- **getpass**: Secure password input (standard library)

## License

This project is provided as-is for educational and development purposes.