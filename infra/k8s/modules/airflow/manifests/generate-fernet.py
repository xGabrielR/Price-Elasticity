import json
from cryptography.fernet import Fernet

def generate_fernet_key():
    fernet_key = Fernet.generate_key().decode()
    return(json.dumps({"output": fernet_key}))

print(generate_fernet_key())