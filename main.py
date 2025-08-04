from autholas import authenticate, get_hardware_id
import getpass

if __name__ == "__main__":
    print("═══════════════════════════════════")
    print("       Autholas Login System       ")
    print("        Python Example Code        ")
    print("═══════════════════════════════════")
    
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hwid = get_hardware_id()
    
    print(f"Device ID: {hwid[:8]}...")
    
    result = authenticate(username, password, hwid)
    
    if result['success']:
        print("\nAuthentication successful!")
        print("Starting application...")
        # Your app logic here
    else:
        print("\nAuthentication failed.")
        input("Press Enter to exit...")