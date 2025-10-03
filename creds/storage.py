import os
import json
from cryptography.fernet import Fernet
from cfg.settings import KEY_FILE, CREDS_FILE

def _write_file_secure(path: str, data: bytes) -> None:
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass

def load_key() -> bytes:
    with open(KEY_FILE, "rb") as f:
        return f.read()

def load_credentials():
    if not os.path.exists(KEY_FILE) or not os.path.exists(CREDS_FILE):
        raise RuntimeError("Credentials not initialized. Run creds/init_creds.py first.")
    key = load_key()
    f = Fernet(key)
    with open(CREDS_FILE, "rb") as fh:
        enc = fh.read()
    dec = f.decrypt(enc)
    return json.loads(dec.decode())
