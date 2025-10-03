import os, json, getpass
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

def init_credentials():
    if os.path.exists(KEY_FILE) and os.path.exists(CREDS_FILE):
        return

    print("GitHub Releases API — init credentials")
    owner = input("Owner (user/org): ").strip()
    repo = input("Repo name: ").strip()
    token = getpass.getpass("PAT (hidden): ").strip()

    key = Fernet.generate_key()
    _write_file_secure(KEY_FILE, key)
    fernet = Fernet(key)

    payload = json.dumps({"owner": owner, "repo": repo, "token": token}).encode()
    encrypted = fernet.encrypt(payload)
    _write_file_secure(CREDS_FILE, encrypted)

    print("Credentials saved securely.")

if __name__ == "__main__":
    init_credentials()
    print("Done.")
