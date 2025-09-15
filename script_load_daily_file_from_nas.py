import requests

# === Replace with your own details ===
QUICKCONNECT_ID = 'nexretail-hsinchu'
USERNAME = 'nexretail'
PASSWORD = 'Nex12Retail34'
FOLDER_PATH = '/'

# Step 1: Discover your NAS's address via QuickConnect
def resolve_quickconnect(quickconnect_id):
    resp = requests.get(f'http://quickconnect.to/{quickconnect_id}')
    print(resp)
    print(resp.__dict__)
    data = resp.json()
    if data['success']:
        # We get the relay/fallback domain here
        url_path = data['server'] + data['path']
        return f"https://{url_path}/webapi/"
    else:
        raise Exception("QuickConnect ID resolution failed")

# Step 2: Login and get session ID
def login(base_url, username, password):
    api_url = base_url + "auth.cgi"
    params = {
        "api": "SYNO.API.Auth",
        "version": "6",
        "method": "login",
        "account": username,
        "passwd": password,
        "session": "FileStation",
        "format": "sid"
    }
    r = requests.get(api_url, params=params)
    r.raise_for_status()
    data = r.json()
    if not data['success']:
        raise Exception("Login failed")
    return data['data']['sid']

# Step 3: List files
def list_files(base_url, sid, folder_path):
    api_url = base_url + "entry.cgi"
    params = {
        "api": "SYNO.FileStation.List",
        "version": "2",
        "method": "list",
        "folder_path": folder_path,
        "_sid": sid
    }
    r = requests.get(api_url, params=params)
    r.raise_for_status()
    data = r.json()
    if not data['success']:
        raise Exception("Failed to list files")
    return data['data']['files']

# === Run it ===
try:
    print("starting NAS file listing process...")
    base_url = resolve_quickconnect(QUICKCONNECT_ID)
    print(f"Resolved QuickConnect to: {base_url}")
    sid = login(base_url, USERNAME, PASSWORD)
    print("Login successful.")
    files = list_files(base_url, sid, FOLDER_PATH)
    for f in files:
        print(f"{f['name']} - {'Directory' if f['isdir'] else 'File'}")
except Exception as e:
    print(f"Error: {e}")
