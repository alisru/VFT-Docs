import os
import subprocess
import base64
import hashlib
import json

def generate_key_and_id():
    print("Generating RSA private key...")
    private_key_path = "key.pem"
    
    # Common Windows OpenSSL paths
    openssl_paths = [
        "openssl", # Check system PATH first
        r"C:\Program Files\Git\usr\bin\openssl.exe",
        r"C:\Program Files (x86)\Git\usr\bin\openssl.exe",
        r"C:\Program Files\Git\bin\openssl.exe"
    ]
    
    openssl_cmd = None
    for path in openssl_paths:
        if path == "openssl":
            # Test if it runs
            try:
                subprocess.run([path, "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                openssl_cmd = path
                break
            except FileNotFoundError:
                continue
        elif os.path.exists(path):
            openssl_cmd = path
            break
            
    if not openssl_cmd:
        print("Error: OpenSSL executable not found.")
        print("Please install Git or OpenSSL, or ensure it is accessible.")
        return
        
    print(f"Using OpenSSL at: {openssl_cmd}")
    try:
        subprocess.run([openssl_cmd, "genrsa", "-out", private_key_path, "2048"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Error running openssl to generate key: {e}")
        return

    print("Extracting public key in DER format...")
    # Extract public key in DER format
    try:
        proc = subprocess.Popen(
            [openssl_cmd, "rsa", "-in", private_key_path, "-pubout", "-outform", "DER"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        der_data, err = proc.communicate()
        if proc.returncode != 0:
            print(f"Error extracting public key: {err.decode()}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Base64 encode the DER public key
    public_key_base64 = base64.b64encode(der_data).decode('utf-8')

    # Calculate Chrome Extension ID from DER public key
    # Chrome uses SHA256 of the DER public key, takes first 32 hex chars, and maps 0-f to a-p
    sha = hashlib.sha256(der_data).hexdigest()
    
    # Take the first 32 chars of the SHA256 hash
    id_part = sha[:32]
    
    # Map hex characters (0-9, a-f) to (a-p)
    # Hex chars: 0123456789abcdef
    # Target chars: abcdefghijklmnop
    mapping = {
        '0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5': 'f', '6': 'g', '7': 'h',
        '8': 'i', '9': 'j', 'a': 'k', 'b': 'l', 'c': 'm', 'd': 'n', 'e': 'o', 'f': 'p'
    }
    
    extension_id = "".join(mapping[c] for c in id_part)
    
    print(f"\nSuccess!")
    print(f"Generated Extension ID: {extension_id}")
    
    # Update manifest.json
    manifest_path = "manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        manifest["key"] = public_key_base64
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            
        print("Updated manifest.json with the new stable public key.")
    else:
        print("manifest.json not found in current directory.")

if __name__ == "__main__":
    generate_key_and_id()
